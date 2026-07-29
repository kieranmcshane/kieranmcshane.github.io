"""Deterministic paper-trading audit for frozen prediction-market quotes.

This module never sends an order.  It replays only contemporaneous model
probabilities and executable top-of-book evidence already frozen in the public
sport payloads.  Missing price, depth, fee, or timestamp evidence produces an
explicit no-bet decision rather than an imputed fill.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path


STRATEGY_SCHEMA_VERSION = "1.0.0"
MODEL_NAMES = ("elo", "glicko2", "trueskill", "robust")
MODEL_LABELS = {
    "elo": "Elo",
    "glicko2": "Glicko-2",
    "trueskill": "Gaussian TrueSkill",
    "robust": "Robust TrueSkill",
}
DEFAULT_STRATEGY = {
    "id": "first-eligible-long-yes-quarter-kelly",
    "version": STRATEGY_SCHEMA_VERSION,
    "initial_bankroll_usd": 1000.0,
    "kelly_fraction": 0.25,
    "minimum_edge": 0.05,
    "maximum_trade_bankroll_fraction": 0.02,
    "maximum_event_bankroll_fraction": 0.10,
    "maximum_reported_liquidity_fraction": 0.01,
    "side": "buy_yes",
    "entry_rule": (
        "For each provider, model, competition, and season, inspect dated snapshots "
        "chronologically. At the first snapshot with complete execution evidence, choose "
        "the participant with the largest fee-adjusted model edge. Buy once only when the "
        "edge is at least five percentage points; otherwise wait for the next snapshot."
    ),
    "fill_rule": (
        "Assume a taker fill only up to the quantity frozen at the best Yes ask. "
        "This is a counterfactual paper fill, not evidence that an order was sent or "
        "that the quote survived network latency."
    ),
    "portfolio_rule": (
        "Each model has an independent USD 1,000 virtual cash account. Stakes use quarter "
        "Kelly and are capped at 2% of current cash, 10% of initial bankroll per event, 1% of reported "
        "liquidity, and frozen top-of-book size."
    ),
}


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value.casefold())
    )


def _ceil_centicent(value: float) -> float:
    return math.ceil(max(value, 0.0) * 10000.0 - 1e-12) / 10000.0


def _fee(provider_name: str, quote: dict, contracts: float, price: float) -> tuple[float | None, str]:
    provider = provider_name.casefold()
    if provider == "polymarket":
        rate = quote.get("taker_fee_rate")
        if not isinstance(rate, (int, float)):
            return None, "missing_provider_fee"
        return round(
            contracts * float(rate) * price * (1.0 - price),
            5,
        ), "quadratic_round_5dp"
    if provider == "kalshi":
        fee_type = quote.get("fee_type")
        multiplier = quote.get("fee_multiplier")
        base_rate = quote.get("taker_fee_base_rate")
        if fee_type not in {"quadratic", "quadratic_with_maker_fees"}:
            return None, "unsupported_provider_fee"
        if not isinstance(multiplier, (int, float)) or not isinstance(base_rate, (int, float)):
            return None, "missing_provider_fee"
        return _ceil_centicent(
            float(base_rate) * float(multiplier) * contracts * price * (1.0 - price)
        ), "quadratic_ceil_centicent"
    return None, "unknown_provider"


def _fee_adjusted_cost(provider_name: str, quote: dict, price: float) -> tuple[float | None, str]:
    fee, method = _fee(provider_name, quote, 1.0, price)
    if fee is None:
        return None, method
    cost = price + fee
    return (cost if 0 < cost < 1 else None), method


def _settlement_map(history: list[dict]) -> dict[tuple[str, str], dict]:
    settlements = {}
    for entry in history:
        resolution = entry.get("resolution")
        if not resolution:
            continue
        key = (
            str(entry.get("competition_id", "")),
            str(entry.get("competition_season", "")),
        )
        settlements[key] = {
            "winner_id": resolution.get("winner_id"),
            "winner_name": resolution.get("winner_name"),
            "resolved_at": resolution.get("resolved_at"),
        }
    return settlements


def _candidate(
    provider_name: str,
    entry: dict,
    model_name: str,
) -> tuple[dict | None, str]:
    forecast = entry.get("model_forecasts", {}).get(model_name, {}).get("probabilities", {})
    quotes = entry.get("execution_quotes") or []
    if not forecast:
        return None, "missing_simultaneous_model_forecast"
    candidates = []
    rejected_reasons = set()
    captured_at = _timestamp(entry.get("captured_at"))
    for quote in quotes:
        entity_id = quote.get("entity_id")
        model_probability = forecast.get(entity_id)
        if not isinstance(model_probability, (int, float)):
            continue
        ask = quote.get("best_ask")
        ask_size = quote.get("top_ask_size")
        quote_at = _timestamp(quote.get("book_captured_at"))
        request_at = _timestamp(quote.get("request_started_at"))
        response_at = _timestamp(quote.get("response_received_at"))
        if not isinstance(ask, (int, float)) or not 0 < ask < 1:
            rejected_reasons.add("missing_executable_ask")
            continue
        if not isinstance(ask_size, (int, float)) or ask_size <= 0:
            rejected_reasons.add("missing_top_of_book_depth")
            continue
        if captured_at is None or quote_at is None or request_at is None or response_at is None:
            rejected_reasons.add("missing_quote_timestamp")
            continue
        if not (request_at <= response_at <= captured_at):
            rejected_reasons.add("non_monotonic_quote_timestamp")
            continue
        if quote_at != response_at:
            rejected_reasons.add("capture_time_differs_from_response_time")
            continue
        if (captured_at - quote_at).total_seconds() > 900:
            rejected_reasons.add("quote_outside_15_minute_capture_window")
            continue
        if not _is_sha256(quote.get("response_sha256")):
            rejected_reasons.add("missing_orderbook_response_hash")
            continue
        fee_request_at = _timestamp(quote.get("fee_request_started_at"))
        fee_response_at = _timestamp(quote.get("fee_response_received_at"))
        if (
            fee_request_at is None
            or fee_response_at is None
            or not _is_sha256(quote.get("fee_response_sha256"))
        ):
            rejected_reasons.add("missing_fee_response_provenance")
            continue
        if not (fee_request_at <= fee_response_at <= captured_at):
            rejected_reasons.add("non_monotonic_fee_timestamp")
            continue
        fee_adjusted_cost, fee_method = _fee_adjusted_cost(
            provider_name,
            quote,
            float(ask),
        )
        if fee_adjusted_cost is None:
            rejected_reasons.add(fee_method)
            continue
        edge = float(model_probability) - fee_adjusted_cost
        candidates.append(
            {
                "entity_id": entity_id,
                "entity_name": quote.get("name"),
                "market_id": quote.get("market_id"),
                "token_id": quote.get("token_id"),
                "model_probability": round(float(model_probability), 6),
                "best_bid": quote.get("best_bid"),
                "best_ask": round(float(ask), 6),
                "top_ask_size": round(float(ask_size), 6),
                "book_captured_at": quote.get("book_captured_at"),
                "request_started_at": quote.get("request_started_at"),
                "response_received_at": quote.get("response_received_at"),
                "retrieval_latency_ms": quote.get("retrieval_latency_ms"),
                "retrieval_url": quote.get("retrieval_url"),
                "response_sha256": quote.get("response_sha256"),
                "book_hash": quote.get("book_hash"),
                "reported_liquidity_usd": quote.get("liquidity_usd"),
                "fee_type": quote.get("fee_type"),
                "fee_multiplier": quote.get("fee_multiplier"),
                "provider_base_fee_bps": quote.get("provider_base_fee_bps"),
                "taker_fee_base_rate": quote.get("taker_fee_base_rate"),
                "fee_schedule_effective_at": quote.get("fee_schedule_effective_at"),
                "fee_schedule_checked_at": quote.get("fee_schedule_checked_at"),
                "fee_schedule_url": quote.get("fee_schedule_url"),
                "fee_request_started_at": quote.get("fee_request_started_at"),
                "fee_response_received_at": quote.get("fee_response_received_at"),
                "fee_response_sha256": quote.get("fee_response_sha256"),
                "taker_fee_rate": quote.get("taker_fee_rate"),
                "fee_method": fee_method,
                "fee_adjusted_cost_per_contract": round(fee_adjusted_cost, 6),
                "edge": round(edge, 6),
            }
        )
    if not candidates:
        reason = sorted(rejected_reasons)[0] if rejected_reasons else "no_overlapping_execution_quote"
        return None, reason
    candidates.sort(key=lambda row: (-row["edge"], row["entity_name"] or ""))
    return candidates[0], "candidate_available"


def build_provider_paper_audit(
    history: list[dict],
    provider_name: str,
    *,
    strategy: dict | None = None,
) -> dict:
    """Replay one provider history into explicit bet and no-bet decisions."""
    config = dict(DEFAULT_STRATEGY)
    if strategy:
        config.update(strategy)
    settlements = _settlement_map(history)
    ordered = sorted(
        history,
        key=lambda row: (
            row.get("captured_at", ""),
            row.get("competition_id", ""),
            str(row.get("competition_season", "")),
        ),
    )
    decisions = []
    positions = []
    entered: set[tuple[str, str, str]] = set()
    cash = {model_name: float(config["initial_bankroll_usd"]) for model_name in MODEL_NAMES}
    event_exposure: dict[tuple[str, str, str], float] = defaultdict(float)

    def settle_due(cutoff: datetime | None = None, *, settle_all: bool = False) -> None:
        for position in positions:
            if position["status"] != "open":
                continue
            key = (
                str(position.get("competition_id", "")),
                str(position.get("competition_season", "")),
            )
            settlement = settlements.get(key)
            resolved_at = _timestamp((settlement or {}).get("resolved_at"))
            if not settlement or (not settle_all and (resolved_at is None or cutoff is None or resolved_at > cutoff)):
                continue
            won = settlement.get("winner_id") == position["entity_id"]
            payout = position["contracts"] if won else 0.0
            pnl = payout - position["total_cost_usd"]
            position.update(
                {
                    "status": "resolved",
                    "winner_id": settlement.get("winner_id"),
                    "winner_name": settlement.get("winner_name"),
                    "resolved_at": settlement.get("resolved_at"),
                    "won": won,
                    "payout_usd": round(payout, 6),
                    "pnl_usd": round(pnl, 6),
                }
            )
            cash[position["model"]] += payout

    for entry in ordered:
        settle_due(_timestamp(entry.get("captured_at")))
        competition_key = (
            str(entry.get("competition_id", "")),
            str(entry.get("competition_season", "")),
        )
        for model_name in MODEL_NAMES:
            entry_key = (*competition_key, model_name)
            if entry_key in entered:
                continue
            candidate, reason = _candidate(provider_name, entry, model_name)
            decision = {
                "decision_id": _sha256(
                    [
                        provider_name,
                        model_name,
                        entry.get("competition_id"),
                        entry.get("competition_season"),
                        entry.get("captured_at"),
                    ]
                )[:20],
                "provider": provider_name,
                "model": model_name,
                "model_label": MODEL_LABELS[model_name],
                "competition_id": entry.get("competition_id"),
                "competition_label": entry.get("competition_label"),
                "competition_season": entry.get("competition_season"),
                "event_id": entry.get("event_id"),
                "event_title": entry.get("event_title"),
                "event_url": entry.get("event_url"),
                "captured_at": entry.get("captured_at"),
                "snapshot_sha256": entry.get("snapshot_sha256"),
                "action": "no_bet",
                "reason": reason,
                "candidate": candidate,
            }
            if candidate is None:
                decisions.append(decision)
                continue
            edge = candidate["edge"]
            if edge < float(config["minimum_edge"]):
                decision["reason"] = "edge_below_threshold"
                decisions.append(decision)
                continue
            cost = candidate["fee_adjusted_cost_per_contract"]
            raw_kelly = max(0.0, (candidate["model_probability"] - cost) / (1.0 - cost))
            applied_kelly = raw_kelly * float(config["kelly_fraction"])
            available_cash = cash[model_name]
            event_key = (*competition_key, model_name)
            caps = {
                "fractional_kelly_usd": available_cash * applied_kelly,
                "maximum_trade_usd": available_cash
                * float(config["maximum_trade_bankroll_fraction"]),
                "maximum_event_remaining_usd": max(
                    0.0,
                    float(config["initial_bankroll_usd"])
                    * float(config["maximum_event_bankroll_fraction"])
                    - event_exposure[event_key],
                ),
                "top_of_book_usd": candidate["top_ask_size"] * candidate["best_ask"],
            }
            liquidity = candidate.get("reported_liquidity_usd")
            if isinstance(liquidity, (int, float)) and liquidity > 0:
                caps["reported_liquidity_usd"] = (
                    float(liquidity) * float(config["maximum_reported_liquidity_fraction"])
                )
            budget = min(caps.values())
            approximate_contracts = budget / max(cost, 1e-9)
            contracts = min(approximate_contracts, candidate["top_ask_size"])
            fee, fee_method = _fee(
                provider_name,
                candidate,
                contracts,
                candidate["best_ask"],
            )
            if fee is None:
                decision["reason"] = fee_method
                decisions.append(decision)
                continue
            principal = contracts * candidate["best_ask"]
            total_cost = principal + fee
            if total_cost <= 0 or total_cost > available_cash + 1e-9:
                decision["reason"] = "stake_not_fundable"
                decisions.append(decision)
                continue
            cash[model_name] -= total_cost
            event_exposure[event_key] += total_cost
            entered.add(entry_key)
            position = {
                "position_id": decision["decision_id"],
                "provider": provider_name,
                "model": model_name,
                "competition_id": entry.get("competition_id"),
                "competition_season": entry.get("competition_season"),
                "entity_id": candidate["entity_id"],
                "entity_name": candidate["entity_name"],
                "market_id": candidate["market_id"],
                "captured_at": entry.get("captured_at"),
                "contracts": round(contracts, 6),
                "execution_price": candidate["best_ask"],
                "principal_usd": round(principal, 6),
                "fee_usd": round(fee, 6),
                "total_cost_usd": round(total_cost, 6),
                "raw_kelly": round(raw_kelly, 6),
                "applied_kelly": round(applied_kelly, 6),
                "bankroll_cash_before_usd": round(available_cash, 6),
                "bankroll_cash_after_entry_usd": round(cash[model_name], 6),
                "caps_usd": {key: round(value, 6) for key, value in caps.items()},
                "status": "open",
            }
            positions.append(position)
            decision.update(
                {
                    "action": "paper_buy_yes",
                    "reason": "first_eligible_edge",
                    "raw_kelly": round(raw_kelly, 6),
                    "applied_kelly": round(applied_kelly, 6),
                    "contracts": round(contracts, 6),
                    "principal_usd": round(principal, 6),
                    "fee_usd": round(fee, 6),
                    "total_cost_usd": round(total_cost, 6),
                    "binding_cap": min(caps, key=caps.get),
                }
            )
            decisions.append(decision)

    settle_due(settle_all=True)
    portfolios = []
    for model_name in MODEL_NAMES:
        rows = [row for row in positions if row["model"] == model_name]
        resolved = [row for row in rows if row["status"] == "resolved"]
        open_rows = [row for row in rows if row["status"] == "open"]
        total_staked = sum(row["total_cost_usd"] for row in rows)
        realized_pnl = sum(row.get("pnl_usd", 0.0) for row in resolved)
        portfolios.append(
            {
                "model": model_name,
                "model_label": MODEL_LABELS[model_name],
                "initial_bankroll_usd": config["initial_bankroll_usd"],
                "cash_usd": round(cash[model_name], 6),
                "open_cost_usd": round(sum(row["total_cost_usd"] for row in open_rows), 6),
                "bets": len(rows),
                "resolved_bets": len(resolved),
                "open_bets": len(open_rows),
                "wins": sum(bool(row.get("won")) for row in resolved),
                "total_staked_usd": round(total_staked, 6),
                "realized_pnl_usd": round(realized_pnl, 6),
                "realized_roi_on_staked": (
                    round(realized_pnl / sum(row["total_cost_usd"] for row in resolved), 6)
                    if resolved
                    else None
                ),
            }
        )
    report_core = {
        "audit_schema_version": STRATEGY_SCHEMA_VERSION,
        "provider": provider_name,
        "status": (
            "scored"
            if any(row["resolved_bets"] for row in portfolios)
            else "collecting_executable_history"
        ),
        "strategy": config,
        "history_snapshots": len(history),
        "decisions": decisions,
        "positions": positions,
        "portfolios": portfolios,
        "limitations": [
            "No real order is sent; a paper fill assumes the frozen top-of-book quote remained available during network latency.",
            "Only the frozen best ask and its displayed size are used; no unobserved depth or midpoint is treated as executable.",
            "Old snapshots without contemporaneous price, depth, fee, and timestamp evidence are excluded and never backfilled.",
            "Returns are descriptive audit evidence, not investment advice or proof of future profitability.",
        ],
    }
    report_core["audit_sha256"] = _sha256(report_core)
    return report_core


def build_market_strategy_report(data_dir: Path) -> dict:
    """Recompute every provider audit from the public frozen histories."""
    audits = []
    input_payloads = []
    for sport in ("tennis", "football", "national-football", "chess"):
        path = data_dir / f"{sport}.json"
        if not path.exists():
            continue
        payload_bytes = path.read_bytes()
        input_payloads.append(
            {
                "sport": sport,
                "filename": path.name,
                "sha256": hashlib.sha256(payload_bytes).hexdigest(),
            }
        )
        payload = json.loads(payload_bytes)
        predictor = payload.get("tournament_predictor") or {}
        for key, provider in (
            ("market_comparison", "Polymarket"),
            ("kalshi_comparison", "Kalshi"),
        ):
            comparison = predictor.get(key) or {}
            embedded = comparison.get("paper_trading")
            if embedded:
                rebuilt = build_provider_paper_audit(
                    comparison.get("history") or [],
                    provider,
                    strategy=embedded.get("strategy"),
                )
                audits.append(
                    {
                        "sport": sport,
                        "provider": provider,
                        "status": (
                            "pass"
                            if rebuilt["audit_sha256"] == embedded.get("audit_sha256")
                            else "fail"
                        ),
                        "embedded_audit_sha256": embedded.get("audit_sha256"),
                        "recomputed_audit_sha256": rebuilt["audit_sha256"],
                        "audit": rebuilt,
                    }
                )
    report = {
        "audit_schema_version": STRATEGY_SCHEMA_VERSION,
        "generated_from": "published sport JSON",
        "engine_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_payloads": input_payloads,
        "reproduction_command": (
            "python3 scripts/audit_market_strategies.py "
            "--public-base https://kieranmcshane.github.io/assets/data/rating-lab "
            "--output market-strategy-report.json --strict"
        ),
        "status": (
            "pass"
            if audits and all(row["status"] == "pass" for row in audits)
            else "incomplete" if not audits else "fail"
        ),
        "audits": audits,
    }
    report["audit_sha256"] = _sha256(report)
    return report


def write_market_strategy_report(data_dir: Path, output: Path) -> dict:
    report = build_market_strategy_report(data_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report
