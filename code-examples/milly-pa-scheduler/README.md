# Scheduled PA Announcements — Safe Python Demonstration

This directory contains an **AI-assisted, sanitized portfolio adaptation** of one part of a real household voice-automation project. It illustrates deterministic schedule matching, local state tracking, dry-run testing, and mock duplicate prevention.

**It is not the production `scheduler.py`.** No production code, credentials, hostnames, internal addresses, family messages, or network dependencies are included. The example cannot send audio and has **no HTTP/network code**.

## Technical context

The real project used a separate Linux cron job with `flock`, a Python JSON schedule, a state marker written after a successful announcement-client call, and an existing authenticated PA stack. This demonstration keeps the local matching/state concepts but **replaces the real announcement client with an injected callback**. It intentionally omits production services and does not prove production uptime or speaker delivery.

## Run locally

Requirements: Python 3.9+ with `zoneinfo` and an IANA timezone database. On some Windows installations, installing the Python `tzdata` package may be needed. No infrastructure credentials are required.

```bash
python3 scheduler_demo.py --at "2026-11-16 10:15"
python3 scheduler_demo.py --at "2026-11-21 10:15"
python3 -m unittest -v test_scheduler_demo.py
```

The first command prints a due sample notice (dry-run only); the second skips a weekend. Tests create disposable temporary files and inject mock queue callbacks.

To *simulate* queue persistence in this demo folder without sending any audio:

```bash
python3 scheduler_demo.py --at "2026-11-16 10:15" --simulate-queue
python3 scheduler_demo.py --at "2026-11-16 10:15" --simulate-queue
```

The first invocation writes a local `demo-delivery-state.json` marker; the second skips the same occurrence. This file is disposable sample state, **not a production status record**.

## What the automated tests cover

- A matching weekday announcement is selected.
- Dry-run mode never writes delivery state.
- Weekends and unmatched minutes are skipped.
- A successful mock queue callback records a marker.
- Repeating an occurrence does not invoke the mock queue twice.
- A failed mock queue callback leaves no false success marker.
- Preexisting markers block requeue attempts without a client call.

## Limitations and transparency

- This version is **not connected** to the Mumble broadcaster, SSH tunnel, or TTS service.
- Tests do not validate live API behavior or speaker playback.
- Real-system duplicate prevention was **best-effort**: a crash between server queue acceptance and a local marker could still cause duplicates. The actual cron used `flock`, whereas this demo only illustrates state behavior, not process locking.
- The project used AI-assisted development under Kevin Mays's architectural control, testing, and approval. This standalone demonstration was prepared as a public-safe adaptation rather than represented as a byte-for-byte production code release.

For the real project's architecture and historical verification record, see the [case study](../../case-studies/milly-household-pa.md) and [verification notes](../../evidence/milly-household-pa-verification.md).

