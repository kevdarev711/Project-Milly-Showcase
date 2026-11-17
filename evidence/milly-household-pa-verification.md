# Milly Household PA — Verification Evidence

**Evidence cutoff:** 11/16/2026  
**System status:** Phases 0–3 accepted by project owner; one-day operational pilot scheduled for 11/17/2026 and **pending**.  
**Evidence provenance:** Historical development records and owner confirmation, consolidated in the technical handoff. **Not** a fresh remote-server inspection, an independent third-party audit, or a guarantee of continuous operation.

## Result types used here

- **Code/configuration inspection:** Behavior visible in reviewed source or configuration; not necessarily a live integration test.
- **Isolated test / dry run:** Test without actual PA transmission, or using a mocked announcement client.
- **Runtime observation:** Server or process response observed in documented diagnostics.
- **Audible confirmation:** Kevin directly reported hearing a real announcement from a connected endpoint.
- **Accepted milestone:** Kevin approved the outcome under his roadmap. Does not expand the underlying test's scope.

## Evidence matrix

| Area | What was checked | Recorded result | Important qualification |
| --- | --- | --- | --- |
| Scheduling | JSON parsed; Python compiled; five approved times matched; weekend skipped | PASS | Matching used dry-run time simulation |
| Cron execution | Separate cron entry and active daemon; invocation logs | PASS | Cron firing is not proof of audible output |
| Concurrent invocation | A competing `flock` execution | PASS, competing run refused | Does not stop manual runs bypassing the lock |
| Persistent state | Successful mocked queue recorded; repeat skipped | PASS | Test was mocked; state JSON is not an end-to-end acknowledgment |
| Invalid/failed delivery | Mocked PA failure | PASS, returned error with no false queued marker | Real long-term outage behavior not established |
| API authentication | Unauthenticated status rejected; authorized status accepted | HTTP 401 / HTTP 200 | Credentials not published |
| Manual end-to-end speech | Existing client → tunnel → broadcaster → TTS → Mumble → Windows listener | Audible confirmation | Confirmed at one eligible listening endpoint |
| Scheduled audio | Temporary evening announcement at a test minute | Reported successful; owner accepted | Raw final restoration/queue-log output not included in source handoff |
| Disable / resume | Existing authenticated global PA control | HTTP 503 while disabled; reenabled | Disables *all* PA, not only the schedule |
| Recovery | Controlled SSH tunnel restart | Service active; authenticated PA endpoint HTTP 200 | Not every outage type or cold boot was tested |
| Afternoon routine | Two approved messages via immediate manual triggers | Audible confirmation | **Simulation**, not naturally timed afternoon operation |
| Endpoint startup | Windows at-logon task and Mumble rejoin | Confirmed after sign-out/sign-in | Client not ready before interactive login after cold boot |

## Implementation evidence

- A separate Python scheduler reads an approved JSON configuration and stores date/occurrence keys only after the announcement CLI exits successfully.
- A cron entry launches it using `flock -n` in approved weekday windows.
- Existing systemd services supervise the SSH tunnel and PA broadcaster; the broadcaster uses an authenticated API, bounded queue, and allowlisted listeners.
- The pre-existing household coordination scheduler was backed up byte-for-byte and left unchanged during this integration.
- The implementation has a documented minimal rollback for the new schedule, distinct from the broader global PA disable.

## Accuracy boundaries

**Do not infer:** transactionally guaranteed exactly-once playback, delivery acknowledgment at the speaker, full outage recovery, automatic audio at Windows cold boot before login, fully automated retry/catch-up, production-wide service reliability metrics, or completed pilot observations.

The handoff explicitly reports that HTTP 202 means **queued**, not **heard**. Manual and controlled audio confirmations are recorded separately. Actual receipt of all five normal-time events remains part of the pending one-day pilot.

## Pilot follow-up (not completed in this evidence cutoff)

The owner-approved pilot is scheduled for **11/17/2026**. After it is actually observed, update a *separate* pilot-results record with the number of on-time, missed, late, and duplicate announcements; speaker coverage; any disruption; and the owner's keep/pause/discontinue decision. Do not enter zero failures until verified. The authoritative roadmap remains owner-maintained.

**Source basis:** Private owner-maintained roadmap export and 11/16/2026 technical handoff. No credentials, internal network details, or household identities reproduced.
