"""Reproducible, offline audit packets for Rating Lab model outputs.

The public sport payload is intentionally compact.  An audit packet keeps the
normalized replay input and the one-step-ahead evaluation ledger needed to
recompute parameter selection and evaluation metrics without contacting an
upstream provider.  Packets are deterministic gzip files: identical inputs and
code produce identical bytes.
"""

from __future__ import annotations

from datetime import date
import gzip
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import Match


AUDIT_SCHEMA_VERSION = "1.0.0"
AUDIT_REPLAY_ORDER = ["date", "entity_a", "entity_b", "competition", "score_a"]


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def match_record(match: Match) -> dict:
    return {
        "date": match.date.isoformat(),
        "entity_a": match.entity_a,
        "entity_b": match.entity_b,
        "score_a": match.score_a,
        "competition": match.competition,
        "season": match.season,
        "home_advantage": match.home_advantage,
        "metadata": dict(sorted(match.metadata.items())),
    }


def normalized_match_records(matches: Iterable[Match]) -> list[dict]:
    return [match_record(match) for match in matches]


def prediction_ledger(
    predictions_by_model: dict[str, list[dict]],
    evaluation_start: date,
) -> list[list]:
    """Return aligned compact rows: date, actual, then model probabilities."""
    model_names = tuple(predictions_by_model)
    lengths = {len(predictions_by_model[name]) for name in model_names}
    if len(lengths) != 1:
        raise ValueError("Audit predictions do not cover the same replay results")
    ledger = []
    for rows in zip(*(predictions_by_model[name] for name in model_names)):
        signatures = {(row["date"], row["actual"]) for row in rows}
        if len(signatures) != 1:
            raise ValueError("Audit predictions are not chronologically aligned")
        if date.fromisoformat(rows[0]["date"]) < evaluation_start:
            continue
        ledger.append(
            [
                rows[0]["date"],
                rows[0]["actual"],
                *[row["predicted"] for row in rows],
            ]
        )
    return ledger


def encode_packet(packet: dict) -> bytes:
    """Encode a deterministic audit packet (mtime=0 avoids gzip clock drift)."""
    return gzip.compress(canonical_json_bytes(packet) + b"\n", mtime=0)


def decode_packet(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def packet_sha256(packet_bytes: bytes) -> str:
    return hashlib.sha256(packet_bytes).hexdigest()


def build_packet(
    *,
    sport: str,
    methodology_version: str,
    source: dict,
    matches: list[Match],
    validation_start: date,
    evaluation_start: date,
    selection_evidence: dict,
    selected_parameters: dict,
    predictions_by_model: dict[str, list[dict]],
    published_metrics: dict[str, dict],
) -> dict:
    match_rows = normalized_match_records(matches)
    ledger = prediction_ledger(predictions_by_model, evaluation_start)
    model_names = list(predictions_by_model)
    return {
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "sport": sport,
        "methodology_version": methodology_version,
        "replay_order": AUDIT_REPLAY_ORDER,
        "source": {
            "name": source.get("source"),
            "url": source.get("source_url"),
            "license": source.get("license"),
            "snapshot_sha256": source.get("snapshot_sha256"),
            "snapshot_hash_scope": source.get("snapshot_hash_scope"),
        },
        "normalized_replay_input": {
            "sha256": sha256_json(match_rows),
            "matches": match_rows,
        },
        "splits": {
            "validation_start": validation_start.isoformat(),
            "evaluation_start": evaluation_start.isoformat(),
            "warmup_matches": sum(match.date < validation_start for match in matches),
            "validation_matches": sum(
                validation_start <= match.date < evaluation_start for match in matches
            ),
            "evaluation_matches": sum(match.date >= evaluation_start for match in matches),
        },
        "parameter_selection": selection_evidence,
        "selected_parameters": selected_parameters,
        "evaluation_ledger": {
            "columns": ["date", "actual", *model_names],
            "sha256": sha256_json(ledger),
            "rows": ledger,
        },
        "published_metrics": published_metrics,
    }


def _same_number(left: object, right: object, tolerance: float = 5e-7) -> bool:
    if left is None or right is None:
        return left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right)) <= tolerance
    return left == right


def _same_metrics(left: dict, right: dict) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def audit_packet(packet: dict, sport_payload: dict, *, full_replay: bool = True) -> dict:
    """Independently verify one packet and return named pass/fail checks."""
    from .pipeline import (  # Imported lazily to avoid a pipeline import cycle.
        MODEL_NAMES,
        _aligned_model_predictions,
        _fide_incumbent_benchmark,
        _fit_log_opinion_pool,
        _log_opinion_probability,
        _metrics,
        _new_model,
        _paired_log_loss_block_bootstrap,
        _run_model,
    )

    checks: list[dict] = []

    def check(identifier: str, passed: bool, evidence: str) -> None:
        checks.append({"id": identifier, "passed": bool(passed), "evidence": evidence})

    match_rows = packet["normalized_replay_input"]["matches"]
    expected_input_hash = packet["normalized_replay_input"]["sha256"]
    actual_input_hash = sha256_json(match_rows)
    check(
        "normalized_input_hash",
        actual_input_hash == expected_input_hash,
        actual_input_hash,
    )
    matches = [Match.from_dict(row) for row in match_rows]
    stable = sorted(
        matches,
        key=lambda match: (
            match.date,
            match.entity_a,
            match.entity_b,
            match.competition,
            match.score_a,
        ),
    )
    check(
        "stable_replay_order",
        normalized_match_records(matches) == normalized_match_records(stable),
        f"{len(matches)} normalized matches",
    )

    validation_start = date.fromisoformat(packet["splits"]["validation_start"])
    evaluation_start = date.fromisoformat(packet["splits"]["evaluation_start"])
    split_counts = {
        "warmup_matches": sum(match.date < validation_start for match in matches),
        "validation_matches": sum(
            validation_start <= match.date < evaluation_start for match in matches
        ),
        "evaluation_matches": sum(match.date >= evaluation_start for match in matches),
    }
    check(
        "chronological_split_counts",
        all(packet["splits"].get(key) == value for key, value in split_counts.items()),
        json.dumps(split_counts, sort_keys=True),
    )
    check(
        "source_snapshot_link",
        packet["source"].get("snapshot_sha256")
        == sport_payload.get("source", {}).get("snapshot_sha256"),
        str(packet["source"].get("snapshot_sha256") or "missing"),
    )

    ledger = packet["evaluation_ledger"]["rows"]
    ledger_hash = sha256_json(ledger)
    check(
        "evaluation_ledger_hash",
        ledger_hash == packet["evaluation_ledger"]["sha256"],
        ledger_hash,
    )
    columns = packet["evaluation_ledger"]["columns"]
    ledger_predictions: dict[str, list[dict]] = {name: [] for name in columns[2:]}
    for row in ledger:
        for index, model_name in enumerate(columns[2:], 2):
            ledger_predictions[model_name].append(
                {"date": row[0], "actual": row[1], "predicted": row[index]}
            )
    for model_name, rows in ledger_predictions.items():
        recalculated = _metrics(rows, evaluation_start)
        published = sport_payload["models"][model_name]["metrics"]
        check(
            f"published_metrics:{model_name}",
            _same_metrics(recalculated, published),
            (
                f"log_loss={recalculated['log_loss']}; "
                f"brier={recalculated['brier']}; n={recalculated['predictions']}"
            ),
        )

    for model_name, evidence in packet["parameter_selection"].items():
        selectable = [
            index
            for index, candidate in enumerate(evidence["candidates"])
            if candidate["metrics"].get("log_loss") is not None
        ]
        if not selectable:
            internal_selected = (
                evidence["selected_index"]
                if model_name == "ensemble"
                else min(1, len(evidence["candidates"]) - 1)
            )
        elif model_name == "ensemble":
            internal_selected = min(
                selectable,
                key=lambda index: (
                    evidence["candidates"][index]["metrics"]["log_loss"],
                    tuple(
                        evidence["candidates"][index]["parameters"][
                            f"weight_{name}"
                        ]
                        for name in MODEL_NAMES
                    ),
                ),
            )
        else:
            internal_selected = min(
                selectable,
                key=lambda index: (
                    evidence["candidates"][index]["metrics"]["log_loss"],
                    index,
                ),
            )
        selected_parameters = evidence["candidates"][internal_selected]["parameters"]
        check(
            f"selection_evidence:{model_name}",
            internal_selected == evidence["selected_index"]
            and selected_parameters == packet["selected_parameters"][model_name],
            f"selected candidate {internal_selected + 1}/{len(evidence['candidates'])}",
        )

    if full_replay:
        replay_predictions: dict[str, list[dict]] = {}
        for model_name in MODEL_NAMES:
            evidence = packet["parameter_selection"][model_name]
            candidate_results = []
            tuning_matches = [match for match in matches if match.date < evaluation_start]
            for candidate in evidence["candidates"]:
                _states, predictions, _histories = _run_model(
                    tuning_matches,
                    _new_model(model_name, candidate["parameters"], packet["sport"]),
                    packet["sport"],
                    history_entities=set(),
                )
                validation = [
                    row
                    for row in predictions
                    if validation_start
                    <= date.fromisoformat(row["date"])
                    < evaluation_start
                ]
                candidate_results.append(_metrics(validation, validation_start))
            selectable = [
                index
                for index, metrics in enumerate(candidate_results)
                if metrics["log_loss"] is not None
            ]
            selected_index = (
                min(
                    selectable,
                    key=lambda index: (
                        candidate_results[index]["log_loss"],
                        index,
                    ),
                )
                if selectable
                else min(1, len(candidate_results) - 1)
            )
            check(
                f"validation_selection:{model_name}",
                selected_index == evidence["selected_index"]
                and all(
                    _same_metrics(metrics, evidence["candidates"][index]["metrics"])
                    for index, metrics in enumerate(candidate_results)
                ),
                f"selected candidate {selected_index + 1}/{len(candidate_results)}",
            )
            selected = evidence["candidates"][selected_index]["parameters"]
            _states, predictions, _histories = _run_model(
                matches,
                _new_model(model_name, selected, packet["sport"]),
                packet["sport"],
                history_entities=set(),
            )
            replay_predictions[model_name] = predictions

        weights, ensemble_predictions, _candidates = _fit_log_opinion_pool(
            replay_predictions,
            validation_start,
            evaluation_start,
        )
        ensemble_evidence = packet["parameter_selection"]["ensemble"]
        aligned = _aligned_model_predictions(replay_predictions)
        validation_rows = [
            row
            for row in aligned
            if validation_start
            <= date.fromisoformat(row["date"])
            < evaluation_start
        ]
        ensemble_candidate_metrics = []
        for candidate in ensemble_evidence["candidates"]:
            parameters = candidate["parameters"]
            candidate_weights = {
                name: parameters[f"weight_{name}"] for name in MODEL_NAMES
            }
            rows = [
                {
                    "date": row["date"],
                    "actual": row["actual"],
                    "predicted": _log_opinion_probability(
                        row["probabilities"],
                        candidate_weights,
                    ),
                }
                for row in validation_rows
            ]
            ensemble_candidate_metrics.append(_metrics(rows, validation_start))
        ensemble_selectable = [
            index
            for index, metrics in enumerate(ensemble_candidate_metrics)
            if metrics["log_loss"] is not None
        ]
        ensemble_selected_index = (
            min(
                ensemble_selectable,
                key=lambda index: (
                    ensemble_candidate_metrics[index]["log_loss"],
                    tuple(
                        ensemble_evidence["candidates"][index]["parameters"][
                            f"weight_{name}"
                        ]
                        for name in MODEL_NAMES
                    ),
                ),
            )
            if ensemble_selectable
            else ensemble_evidence["selected_index"]
        )
        check(
            "validation_selection:ensemble",
            all(
                _same_number(
                    weights[name],
                    packet["selected_parameters"]["ensemble"][f"weight_{name}"],
                )
                for name in MODEL_NAMES
            )
            and ensemble_selected_index == ensemble_evidence["selected_index"]
            and all(
                _same_metrics(
                    metrics,
                    ensemble_evidence["candidates"][index]["metrics"],
                )
                for index, metrics in enumerate(ensemble_candidate_metrics)
            ),
            (
                f"selected candidate {ensemble_selected_index + 1}/"
                f"{len(ensemble_candidate_metrics)}; "
                f"weights={json.dumps(weights, sort_keys=True)}"
            ),
        )
        replay_predictions["ensemble"] = ensemble_predictions
        replay_ledger = prediction_ledger(replay_predictions, evaluation_start)
        replay_hash = sha256_json(replay_ledger)
        check(
            "full_replay_prediction_hash",
            replay_hash == packet["evaluation_ledger"]["sha256"],
            replay_hash,
        )
        comparison = _paired_log_loss_block_bootstrap(
            replay_predictions,
            evaluation_start,
        )
        check(
            "paired_block_bootstrap",
            canonical_json_bytes(comparison)
            == canonical_json_bytes(sport_payload["evaluation_comparison"]),
            (
                f"{comparison.get('resamples', 0)} resamples; "
                f"{comparison.get('blocks', 0)} calendar-month blocks"
            ),
        )
        if packet["sport"] == "chess":
            benchmark = _fide_incumbent_benchmark(
                matches,
                {name: replay_predictions[name] for name in MODEL_NAMES},
                replay_predictions["ensemble"],
                evaluation_start,
            )
            check(
                "fide_incumbent_benchmark",
                canonical_json_bytes([benchmark])
                == canonical_json_bytes(sport_payload["incumbent_benchmarks"]),
                (
                    f"{benchmark.get('common_evaluation_predictions', 0)} "
                    "common predictions"
                ),
            )

    passed = all(item["passed"] for item in checks)
    return {
        "sport": packet["sport"],
        "status": "pass" if passed else "fail",
        "verification_level": "full_replay" if full_replay else "artifact_integrity",
        "checks": checks,
    }


def write_report(
    data_dir: Path,
    *,
    report_path: Path | None = None,
    full_replay: bool = True,
    auditor_revision: str | None = None,
) -> dict:
    audit_dir = data_dir / "audit"
    results = []
    generated_at_values = []
    manifest_path = data_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    expected_revision = manifest.get("code_revision")
    revision_matches = (
        not expected_revision
        or expected_revision == "unknown"
        or not auditor_revision
        or auditor_revision == "unknown"
        or expected_revision == auditor_revision
    )
    for sport in ("tennis", "football", "national-football", "chess"):
        payload_path = data_dir / f"{sport}.json"
        packet_path = audit_dir / f"{sport}-replay.json.gz"
        if not payload_path.exists() or not packet_path.exists():
            results.append(
                {
                    "sport": sport,
                    "status": "incomplete",
                    "verification_level": "none",
                    "checks": [
                        {
                            "id": "audit_packet_present",
                            "passed": False,
                            "evidence": f"Missing {packet_path.name}",
                        }
                    ],
                }
            )
            continue
        payload = json.loads(payload_path.read_text())
        if payload.get("generated_at"):
            generated_at_values.append(payload["generated_at"])
        packet_bytes = packet_path.read_bytes()
        expected_hash = payload.get("model_audit", {}).get("packet_sha256")
        actual_packet_hash = hashlib.sha256(packet_bytes).hexdigest()
        packet_hash_check = {
            "id": "audit_packet_hash",
            "passed": bool(expected_hash) and actual_packet_hash == expected_hash,
            "evidence": actual_packet_hash,
        }
        try:
            result = audit_packet(
                decode_packet(packet_path),
                payload,
                full_replay=full_replay,
            )
            result["checks"].insert(0, packet_hash_check)
            if not packet_hash_check["passed"]:
                result["status"] = "fail"
        except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
            result = {
                "sport": sport,
                "status": "fail",
                "verification_level": (
                    "full_replay" if full_replay else "artifact_integrity"
                ),
                "checks": [
                    packet_hash_check,
                    {
                        "id": "audit_packet_readable",
                        "passed": False,
                        "evidence": (
                            f"{type(error).__name__}: audit packet could not be verified"
                        ),
                    },
                ],
            }
        if full_replay:
            payload["model_audit"]["status"] = result["status"]
            staged_payload = payload_path.with_name(f".{payload_path.name}.tmp")
            staged_payload.write_text(
                json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n"
            )
            staged_payload.replace(payload_path)
        results.append(result)
    statuses = {result["status"] for result in results}
    overall = (
        "pass"
        if statuses == {"pass"} and revision_matches
        else "incomplete"
        if "incomplete" in statuses and "fail" not in statuses and revision_matches
        else "fail"
    )
    report = {
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "generated_at": max(generated_at_values, default=None),
        "status": overall,
        "verification_level": "full_replay" if full_replay else "artifact_integrity",
        "code": {
            "expected_revision": expected_revision,
            "auditor_revision": auditor_revision,
            "matches": revision_matches,
        },
        "command": (
            "python3 scripts/audit_rating_models.py "
            "--data-dir assets/data/rating-lab --strict"
        ),
        "sports": results,
    }
    destination = report_path or audit_dir / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged = destination.with_name(f".{destination.name}.tmp")
    staged.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    staged.replace(destination)
    return report
