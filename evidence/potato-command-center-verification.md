# Potato Command Center — Historical Verification Record

**Prepared:** 11/16/2026  
**Project:** Potato Command Center / related Network Monitor Potato development  
**Evidence class:** Documentary summary of dated, tracked development results. **Not** a fresh test execution, certified security audit, or raw terminal transcript.

## Scope and source limitations

The verification statements below were transcribed and condensed from the following private source documents supplied by the project owner:

- `pp_Roadmap_Tracked.md` (last updated 11/04/2026)
- `nmp_Roadmap_Tracked.md` (last updated 11/12/2026)

These tracked exports contain dated execution notes, but the original raw logs and working source files were not supplied for independent rerunning when this document was prepared. An outcome is labeled **historical** for this reason. Numbers refer to the recorded test context, not current system state.

## Verification ledger

| Date | Capability | Reported result in source | Evidence level and caveat |
| --- | --- | --- | --- |
| 11/03/2026 | Archive-health checks | Four snapshots passed SHA-256 and structural validation; checker returned exit code 0 | Recorded live-homelab check, not a new run |
| 11/03/2026 | Retention scanner | Read-only scan classified four snapshots as protected because an incident was open; no deletion performed | Recorded live read-only check |
| 11/03/2026 | Retention safety tests | Simulated scenarios covered newest-30 preservation, 90-day age threshold, missing checksum, open-incident protection, and invalid timestamps | Isolated tests; not destructive production tests |
| 11/04/2026 | Unattended collection | First scheduled snapshot execution completed successfully and five archives passed integrity checks | Recorded unattended run |
| 11/04/2026 | ARM64 portable release | 25-file tarball; preflight, installer, dry-run and removal handling, and data preservation tested; archive checksum verified | Isolated package validation |
| 11/04/2026 | ARM64 Debian package | Version 0.1.0-1 installed; isolated upgrade to 0.1.0-2, rollback to 0.1.0-1, removal, and data preservation passed | Isolated package lifecycle validation |
| 11/04/2026 | Authenticated dashboard | Mobile display verified system metrics and archive health; five snapshots and zero integrity problems shown at time of test | Functional point-in-time test; not a security certification |
| 11/10/2026 | Scheduled operations | Snapshot and archive-health watch services executed successfully under user-level systemd timers | Recorded scheduled runs |
| 11/12/2026 | Monitoring integration | Command Center option 14 displayed monitoring status and event history; prior 13 options preserved | Recorded menu integration test |

## Defect and correction example

**Symptom:** Archive discovery did not find files that were present.  
**Cause identified:** A double-escaped filename regular expression.  
**Correction:** Repair the scanner's matching expression, then validate discovery against existing snapshots and checksum companions.  
**Protection:** The correction and retention tests did not modify or delete the production archive.  
**Result:** The corrected scan found the four expected pairs; separate simulated retention safety cases passed.

This is recorded in the 11/03/2026 Potato Project log. It should not be presented as a raw command transcript.

## What remains unverified or unfinished

- No new independent run was performed to prepare this public document.
- No claim is made for commercial uptime, production user counts, disaster-recovery RTO/RPO, or security certification.
- Multi-node automatic failover is not implemented or accepted by the provided tracked project roadmap.
- The newer five-minute availability notification workflow was still awaiting full delivery verification and acceptance as of the latest supplied Network Monitor Potato roadmap.
- Final review should compare these summaries with source records and remove any screenshots/logs containing real IPs, MACs, credentials, private hostnames, or personal data before publication.

## Next high-value artifacts to add (not yet supplied)

1. **Redacted 30–60 second screen recording** showing an authenticated dashboard, a refresh of health metrics, and the Command Center status view. Remove addresses, device names, household details, authentication screens, and tokens.
2. **Redacted timer execution excerpt** showing actual invocation date, exit status, and job name from `systemctl --user` or `journalctl --user`. Verify the live unit names first; do not paste entire journals.
3. **Sanitized, independently runnable code excerpt** taken from an existing Bash/Python utility, with sample inputs, expected output, and tests. Do not publish private config or a fabricated representation of the production script.

*This document is a historical evidence index, not proof that the current live system was freshly inspected.*
