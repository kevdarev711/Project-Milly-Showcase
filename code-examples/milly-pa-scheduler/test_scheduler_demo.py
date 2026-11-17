"""Synthetic unit tests. These do not exercise a live PA endpoint."""

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scheduler_demo import process_minute


class SchedulerDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.config = root / "sample_schedule.json"
        self.state = root / "state.json"
        self.config.write_text(json.dumps({
            "timezone": "UTC",
            "days": [1, 2, 3, 4, 5],
            "announcements": [{
                "id": "demo_notice_a",
                "time": "10:15",
                "message": "Example reminder A."
            }]
        }), encoding="utf-8")
        self.monday_due = datetime(2026, 11, 16, 10, 15, tzinfo=timezone.utc)

    def test_weekday_dry_run_finds_due_message(self):
        result = process_minute(self.config, self.state, self.monday_due)
        self.assertIn("DRY RUN", result[0])
        self.assertIn("Example reminder A.", result[0])

    def test_dry_run_never_writes_state(self):
        process_minute(self.config, self.state, self.monday_due)
        self.assertFalse(self.state.exists())

    def test_weekend_skipped(self):
        saturday = datetime(2026, 11, 21, 10, 15, tzinfo=timezone.utc)
        result = process_minute(self.config, self.state, saturday)
        self.assertIn("Outside configured weekdays", result[0])

    def test_unmatched_minute_skipped(self):
        not_due = datetime(2026, 11, 16, 10, 16, tzinfo=timezone.utc)
        self.assertEqual(process_minute(self.config, self.state, not_due),
                         ["SKIP: No matching announcement"])

    def test_simulated_success_persists_marker(self):
        result = process_minute(self.config, self.state, self.monday_due,
                                queue_fn=lambda _: True, dry_run=False)
        self.assertIn("MOCK QUEUED", result[0])
        state = json.loads(self.state.read_text())
        self.assertEqual(state["2026-11-16:demo_notice_a"], "queued")

    def test_second_attempt_does_not_queue_again(self):
        calls = []

        def record(message):
            calls.append(message)
            return True

        process_minute(self.config, self.state, self.monday_due,
                       queue_fn=record, dry_run=False)
        result = process_minute(self.config, self.state, self.monday_due,
                                queue_fn=record, dry_run=False)
        self.assertEqual(len(calls), 1)
        self.assertIn("Already queued", result[0])

    def test_queue_failure_does_not_mark_success(self):
        result = process_minute(self.config, self.state, self.monday_due,
                                queue_fn=lambda _: False, dry_run=False)
        self.assertIn("ERROR", result[0])
        self.assertFalse(self.state.exists())

    def test_existing_marker_does_not_require_queue_callback(self):
        self.state.write_text(json.dumps({"2026-11-16:demo_notice_a": "queued"}))
        result = process_minute(self.config, self.state, self.monday_due,
                                queue_fn=None, dry_run=False)
        self.assertIn("Already queued", result[0])


if __name__ == "__main__":
    unittest.main()
