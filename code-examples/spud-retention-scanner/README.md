# SPUD Retention Scanner — Read-Only Python Example

A small, **standalone demonstration adapted from an operational script** in Kevin Mays's Potato Command Center. It classifies timestamped backup records without deleting or modifying any files. All paths are provided as command-line arguments; **no household network addresses, credentials, incident history, or production archives are included**.

## What it demonstrates

- Python file discovery (`pathlib`), timestamps, regular expressions, and command-line parsing
- Conservative retention rules: protect when the incident registry is absent/open, protect the newest 30 snapshots, protect those under 90 days old, and require a matching checksum *companion file* for eligibility
- Read-only classification and human-readable reporting
- Reproducible tests using disposable files and a fixed reference time

**Important distinction:** This script verifies the **presence and type** of a `.sha256` companion file. It does **not** compute or compare SHA-256 hashes, delete archives, assess file contents, or enforce a live retention policy. "DRY-RUN ELIGIBLE" is not an instruction to delete anything. An independent archive-health component handles actual checksum integrity in the larger project.

## Run tests

Requires Python 3.9+ and no third-party dependencies.

```bash
python3 -m unittest -v test_retention_scanner.py
```

## Run the CLI against your own disposable example directories

```bash
python3 retention_scanner.py --archive /path/to/test/snapshots --incidents /path/to/test/incidents
```

Use **synthetic test files only** for your first run. A missing incident registry deliberately triggers protection. The CLI never writes to the paths provided.

## Project context and provenance

Adapted from `retention-scan.py` in the independent Potato Command Center project. The original was implemented and validated in the project's November 2026 development records; this portfolio version makes directory locations configurable and adds isolated automated tests without changing the essential retention rules. The original production file is unchanged.

The project uses AI-assisted development and review. Kevin directs scope, reviews proposed changes, validates operating-system behavior, and makes final decisions about deployment. This standalone version was adapted and tested with AI assistance; it should not be represented as entirely independently handwritten code.

## Security and limits

No credentials, private household hostnames, network addresses, or operational records are bundled. This example is educational/read-only and not a drop-in replacement for the production scanner. Paths supplied at runtime are read only; use trusted local test directories. The exact operating-system environment of the live system is intentionally omitted.

