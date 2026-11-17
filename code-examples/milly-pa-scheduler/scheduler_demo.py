#!/usr/bin/env python3
"""Standalone, synthetic demonstration of deterministic PA schedule matching.

This is an AI-assisted portfolio adaptation, NOT the deployed Milly scheduler.
It does not connect to a PA server, read production files, or send audio.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


BASE = Path(__file__).resolve().parent
DEFAULT_CONFIG = BASE / "sample_schedule.json"
DEFAULT_STATE = BASE / "demo-delivery-state.json"


def process_minute(config_file: Path, state_file: Path, now: datetime,
                   queue_fn=None, dry_run: bool = True):
    """Return per-occurrence statuses; queue_fn is an injected *mock* callback.

    Real deployments should independently manage authentication, external queues,
    locking, error recovery, and operational controls.
    """
    config = json.loads(config_file.read_text(encoding="utf-8"))
    zone = ZoneInfo(config["timezone"])
    local_now = now.astimezone(zone)
    if local_now.isoweekday() not in config["days"]:
        return ["SKIP: Outside configured weekdays"]

    state = (json.loads(state_file.read_text(encoding="utf-8"))
             if state_file.exists() else {})
    day = local_now.strftime("%Y-%m-%d")
    minute = local_now.strftime("%H:%M")
    outcomes = []

    for announcement in config["announcements"]:
        if announcement["time"] != minute:
            continue
        key = f"{day}:{announcement['id']}"
        if key in state:
            outcomes.append(f"SKIP: Already queued: {key}")
        elif dry_run:
            outcomes.append(f"DRY RUN: {key} — {announcement['message']}")
        elif queue_fn is None or not queue_fn(announcement["message"]):
            outcomes.append(f"ERROR: Mock queue rejected: {key}")
        else:
            state[key] = "queued"
            temporary = state_file.with_suffix(".tmp")
            temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
            temporary.replace(state_file)
            outcomes.append(f"MOCK QUEUED: {key}")

    return outcomes or ["SKIP: No matching announcement"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--at", help="Synthetic time: YYYY-MM-DD HH:MM in sample timezone")
    parser.add_argument("--simulate-queue", action="store_true",
                        help="Use a local mock queue; writes only demo-delivery-state.json")
    args = parser.parse_args()

    config = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
    zone = ZoneInfo(config["timezone"])
    if args.at:
        now = datetime.strptime(args.at, "%Y-%m-%d %H:%M").replace(tzinfo=zone)
    else:
        now = datetime.now(zone)

    for outcome in process_minute(
        DEFAULT_CONFIG, DEFAULT_STATE, now,
        queue_fn=(lambda _message: True) if args.simulate_queue else None,
        dry_run=not args.simulate_queue,
    ):
        print(outcome)


if __name__ == "__main__":
    main()
