from __future__ import annotations

import unittest
from datetime import date

from scripts.check_rating_lab_delivery import competition_temporal_failures


class RatingLabDeliveryTests(unittest.TestCase):
    def test_overdue_forecast_must_be_delayed_and_empty(self):
        payload = {
            "tournament_predictor": {
                "competitions": [
                    {
                        "id": "unsafe-live-draw",
                        "format": "tennis knockout draw",
                        "state": "live",
                        "status": "live",
                        "state_view": "conditional_forecast",
                        "source_health": "current",
                        "forecast_as_of": "2026-08-31",
                        "forecast_checked_at": "2026-08-23T18:00:00+00:00",
                        "forecast_grace_days": 1,
                        "completed_matches": 44,
                        "remaining_matches": 5,
                        "total_matches": 49,
                        "last_fixture": "2026-08-23",
                        "next_fixture": "2026-08-21",
                        "forecast_available": True,
                        "models": {"elo": {"participants": []}},
                        "settled_performance": {"models": {"elo": {}}},
                    }
                ]
            }
        }

        failures = competition_temporal_failures(payload, as_of=date(2026, 8, 31))

        self.assertTrue(any("overdue" in failure for failure in failures))
        self.assertTrue(any("model probabilities" in failure for failure in failures))
        self.assertTrue(any("performance analysis" in failure for failure in failures))
        self.assertTrue(any("fail-closed" in failure for failure in failures))

    def test_fail_closed_delayed_forecast_passes_delivery_contract(self):
        payload = {
            "tournament_predictor": {
                "competitions": [
                    {
                        "id": "safe-delayed-draw",
                        "format": "tennis knockout draw",
                        "state": "live",
                        "status": "live",
                        "state_view": "forecast_withheld",
                        "source_health": "delayed",
                        "source_health_reason": "Official draw update is overdue.",
                        "forecast_as_of": "2026-08-31",
                        "forecast_checked_at": "2026-08-23T18:00:00+00:00",
                        "forecast_grace_days": 1,
                        "completed_matches": 44,
                        "remaining_matches": 5,
                        "total_matches": 49,
                        "last_fixture": "2026-08-23",
                        "next_fixture": "2026-08-21",
                        "forecast_available": False,
                        "models": {},
                    }
                ]
            }
        }

        self.assertEqual(
            competition_temporal_failures(payload, as_of=date(2026, 8, 31)),
            [],
        )

    def test_finished_competition_cannot_publish_a_next_fixture(self):
        payload = {
            "tournament_predictor": {
                "competitions": [
                    {
                        "id": "finished-event",
                        "format": "round-robin tournament",
                        "state": "finished",
                        "status": "finished",
                        "state_view": "performance",
                        "source_health": "current",
                        "source_health_reason": "All sourced results are current.",
                        "forecast_as_of": "2026-08-31",
                        "forecast_checked_at": "2026-08-31T08:00:00+00:00",
                        "completed_matches": 10,
                        "remaining_matches": 0,
                        "total_matches": 10,
                        "last_fixture": "2026-08-30",
                        "next_fixture": "2026-08-30",
                        "forecast_available": True,
                        "models": {"elo": {}},
                    }
                ]
            }
        }

        failures = competition_temporal_failures(payload, as_of=date(2026, 8, 31))

        self.assertEqual(
            failures,
            ["finished-event is finished but still exposes a next fixture"],
        )


if __name__ == "__main__":
    unittest.main()
