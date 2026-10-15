"""Regression coverage for full-precision ensemble selection in frozen audits."""
from copy import deepcopy
from datetime import date, timedelta
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from rating_lab.audit import audit_packet
from rating_lab.models import Match
from rating_lab.pipeline import MODEL_NAMES, build_sport_payload
from scripts import audit_rating_models


class EnsembleAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Candidates 5 and 9 both publish 0.6802, but candidate 9 has the
        # smaller unrounded loss.  The old auditor incorrectly picks 5.
        outcomes = [
            0, 0, .5, .5, .5, .5, 1, .5, .5, 1, .5, 0,
            1, 0, 1, 0, .5, 0, 0, .5, 0, 0, 1, 0,
            .5, .5, 0, .5, 1, 1, 0, .5, 1, 1, 1, 1,
        ]
        matches = [
            Match(date(2023, 1, 1) + timedelta(days=i * 35),
                  "p1", "p2", float(outcome), "Fixture", "2025", True,
                  {"rating_a": "2400", "rating_b": "2350"})
            for i, outcome in enumerate(outcomes)
        ]
        cls.packet = {}
        cls.payload = build_sport_payload(
            "chess", matches, {"p1": {"name": "One"}, "p2": {"name": "Two"}},
            {"source": "Fixture", "snapshot_sha256": "a" * 64},
            audit_packet=cls.packet,
        )

    def failed_checks(self, packet, *, full_replay=True):
        return {
            check["id"] for check in
            audit_packet(packet, self.payload, full_replay=full_replay)["checks"]
            if not check["passed"]
        }

    def test_rounding_tie_does_not_override_exact_winner(self):
        evidence = self.packet["parameter_selection"]["ensemble"]
        self.assertEqual(evidence["selected_index"], 8)
        losses = [c["metrics"]["log_loss"] for c in evidence["candidates"]]
        self.assertEqual(losses[4], losses[8])
        self.assertEqual(losses[8], min(losses))
        for full_replay in (False, True):
            with self.subTest(full_replay=full_replay):
                self.assertEqual(self.failed_checks(self.packet, full_replay=full_replay), set())

    def test_full_replay_rejects_wrong_winner_even_with_same_rounded_loss(self):
        packet = deepcopy(self.packet)
        evidence = packet["parameter_selection"]["ensemble"]
        evidence["selected_index"] = 4
        packet["selected_parameters"]["ensemble"] = evidence["candidates"][4]["parameters"]
        # Rounded evidence alone cannot distinguish these candidates.
        self.assertEqual(self.failed_checks(packet, full_replay=False), set())
        self.assertIn("validation_selection:ensemble", self.failed_checks(packet))

    def test_artifact_check_rejects_nonminimal_candidate(self):
        packet = deepcopy(self.packet)
        evidence = packet["parameter_selection"]["ensemble"]
        worst = max(range(len(evidence["candidates"])),
                    key=lambda i: evidence["candidates"][i]["metrics"]["log_loss"])
        evidence["selected_index"] = worst
        packet["selected_parameters"]["ensemble"] = evidence["candidates"][worst]["parameters"]
        self.assertIn("selection_evidence:ensemble", self.failed_checks(packet, full_replay=False))

    def test_full_replay_still_rejects_modified_candidate_metrics(self):
        packet = deepcopy(self.packet)
        packet["parameter_selection"]["ensemble"]["candidates"][0]["metrics"]["brier"] += .01
        self.assertIn("validation_selection:ensemble", self.failed_checks(packet))

    def test_no_validation_uses_equal_weights(self):
        packet = {}
        matches = [Match(date(2026, 1, 1), "a", "b", .5, "Fixture")]
        payload = build_sport_payload(
            "chess", matches, {"a": {"name": "A"}, "b": {"name": "B"}},
            {"source": "Fixture"}, audit_packet=packet,
        )
        self.assertTrue(all(packet["selected_parameters"]["ensemble"][f"weight_{name}"] == .25
                            for name in MODEL_NAMES))
        self.assertEqual(audit_packet(packet, payload)["status"], "pass")

    def test_strict_cli_prints_failed_checks_and_returns_nonzero(self):
        report = {"status": "fail", "verification_level": "full_replay", "sports": [
            {"sport": "chess", "status": "fail", "checks": [
                {"id": "validation_selection:ensemble", "passed": False, "evidence": "wrong winner"},
            ]},
        ]}
        output = io.StringIO()
        with patch.object(audit_rating_models, "write_report", return_value=report), \
             patch("sys.argv", ["audit_rating_models.py", "--strict"]), redirect_stdout(output):
            self.assertEqual(audit_rating_models.main(), 1)
        self.assertIn("FAIL validation_selection:ensemble: wrong winner", output.getvalue())
