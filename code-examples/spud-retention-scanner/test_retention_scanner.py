"""Tests use generated disposable data only; never real backup archives."""
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from retention_scanner import classify_snapshots, discover_snapshots


class RetentionScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / "snapshots"
        self.incidents = self.root / "incidents"
        self.archive.mkdir()
        self.incidents.mkdir()
        self.now = datetime(2026, 11, 16, 12, 0, 0)

    def snapshot(self, age_days, paired=True):
        dt = self.now - timedelta(days=age_days)
        name = f"SERVER1-{dt:%Y%m%d-%H%M%S}.txt"
        (self.archive / name).write_text("synthetic snapshot\n", encoding="utf-8")
        if paired:
            (self.archive / (name + ".sha256")).write_text("synthetic companion, not verified\n", encoding="utf-8")
        return name

    def close_incident(self):
        (self.incidents / "INCIDENT-001.md").write_text(
            "- Status: CLOSED\nRecovery verified: YES\n", encoding="utf-8"
        )

    def test_missing_registry_protects_all(self):
        name = self.snapshot(200)
        self.assertEqual(classify_snapshots(self.archive, self.incidents, self.now)[0][1], "PROTECTED")

    def test_open_incident_protects_all(self):
        (self.incidents / "INCIDENT-001.md").write_text(
            "- Status: OPEN\nRecovery verified: NO\n", encoding="utf-8"
        )
        self.snapshot(200)
        self.assertEqual(classify_snapshots(self.archive, self.incidents, self.now)[0][1], "PROTECTED")

    def test_newest_30_protected_older_eligible(self):
        self.close_incident()
        names = [self.snapshot(i + 100) for i in range(31)]
        results = dict((name, (status, reason)) for name, status, reason in classify_snapshots(self.archive, self.incidents, self.now))
        self.assertEqual(results[names[0]][0], "PROTECTED")
        self.assertEqual(results[names[-1]][0], "DRY-RUN ELIGIBLE")

    def test_under_90_days_protected_beyond_newest_30(self):
        self.close_incident()
        younger = self.snapshot(40)
        for i in range(30):
            self.snapshot(i + 1)
        results = dict((name, status) for name, status, _ in classify_snapshots(self.archive, self.incidents, self.now))
        self.assertEqual(results[younger], "PROTECTED")

    def test_missing_checksum_companion_protected(self):
        self.close_incident()
        missing = self.snapshot(200, paired=False)
        for i in range(30):
            self.snapshot(i + 1)
        results = dict((name, status) for name, status, _ in classify_snapshots(self.archive, self.incidents, self.now))
        self.assertEqual(results[missing], "PROTECTED")

    def test_invalid_timestamp_rejected(self):
        (self.archive / "SERVER1-20261399-120000.txt").write_text("x", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "INVALID SNAPSHOT TIMESTAMP"):
            discover_snapshots(self.archive)

    def test_scanner_never_changes_files(self):
        self.close_incident()
        self.snapshot(10)
        before = {p.name: p.read_bytes() for p in self.archive.iterdir()}
        classify_snapshots(self.archive, self.incidents, self.now)
        after = {p.name: p.read_bytes() for p in self.archive.iterdir()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
