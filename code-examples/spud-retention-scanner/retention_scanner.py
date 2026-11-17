#!/usr/bin/env python3
"""SPUD Retention Scanner — standalone, read-only portfolio demonstration.

Adapted from Kevin Mays's operational retention-scan.py. No deletions, writes,
network calls, or checksum-content verification are performed.
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re

KEEP_NEWEST = 30
MIN_AGE_DAYS = 90
SNAPSHOT_PATTERN = re.compile(r"^SERVER1-(\d{8})-(\d{6})(?:-\d+)?\.txt$")


def incident_protection(incidents: Path):
    files = sorted(incidents.glob("INCIDENT-*.md"))
    if not files:
        return True, "Incident registry missing or empty"
    for path in files:
        if path.is_symlink() or not path.is_file():
            return True, "Invalid incident record"
        text = path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^- Status: CLOSED\s*$", text):
            return True, f"Incident not verified closed: {path.name}"
        if not re.search(r"(?m)^Recovery verified: YES\s*$", text):
            return True, f"Recovery not verified: {path.name}"
    return False, "All active-registry incidents closed and verified"


def discover_snapshots(archive: Path):
    results = []
    for path in archive.iterdir():
        match = SNAPSHOT_PATTERN.fullmatch(path.name)
        if not match:
            continue
        try:
            timestamp = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M%S")
        except ValueError as exc:
            raise ValueError(f"INVALID SNAPSHOT TIMESTAMP: {path.name}") from exc
        checksum = archive / (path.name + ".sha256")
        paired = (
            path.is_file() and not path.is_symlink()
            and checksum.is_file() and not checksum.is_symlink()
        )
        results.append((timestamp, path.name, paired))
    return sorted(results, reverse=True)


def classify_snapshots(archive: Path, incidents: Path, now=None):
    protected, incident_reason = incident_protection(incidents)
    snapshots = discover_snapshots(archive)
    now = datetime.now() if now is None else now
    results = []
    for index, (timestamp, name, paired) in enumerate(snapshots):
        age = now - timestamp
        if protected:
            status, reason = "PROTECTED", incident_reason
        elif index < KEEP_NEWEST:
            status, reason = "PROTECTED", "Within newest 30 snapshots"
        elif age < timedelta(days=MIN_AGE_DAYS):
            status, reason = "PROTECTED", "Younger than 90 days"
        elif not paired:
            status, reason = "PROTECTED", "Missing or invalid checksum pair"
        else:
            status, reason = "DRY-RUN ELIGIBLE", "Passed retention eligibility checks"
        results.append((name, status, reason))
    return results


def main():
    parser = argparse.ArgumentParser(description="Read-only snapshot retention classifier")
    parser.add_argument("--archive", required=True, type=Path, help="Directory of example snapshots")
    parser.add_argument("--incidents", required=True, type=Path, help="Directory of example incidents")
    args = parser.parse_args()
    protected, reason = incident_protection(args.incidents)
    print("=== SPUD RETENTION SCANNER — PORTFOLIO DEMO ===")
    print("MODE: READ ONLY — NO DELETION")
    print("INCIDENT PROTECTION:", "ACTIVE" if protected else "CLEAR")
    print("REASON:", reason)
    print("KEEP NEWEST:", KEEP_NEWEST)
    print("MINIMUM AGE:", MIN_AGE_DAYS, "days")
    print("=== RETENTION REPORT ===")
    results = classify_snapshots(args.archive, args.incidents)
    for name, status, why in results:
        print(f"{name} | {status} | {why}")
    print("TOTAL SNAPSHOTS:", len(results))
    print("PROTECTED:", sum(status == "PROTECTED" for _, status, _ in results))
    print("DRY-RUN ELIGIBLE:", sum(status == "DRY-RUN ELIGIBLE" for _, status, _ in results))
    print("NO FILES DELETED OR MODIFIED")


if __name__ == "__main__":
    main()
