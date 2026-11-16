# AI-Assisted Household Automation and Notification System

**Project type:** Independent technical project (AI-assisted development)  
**Status:** Tested features and documented operational workflows; final V2 project acceptance remains pending.  
**Relevant roles:** Junior AI Automation Engineer, AI Integration Specialist, Technical Support Engineer

## Problem

Several practical household coordination tasks—calendar reminders, recurring tasks, scheduled summaries, and notifications—needed a consistent workflow connecting an existing AI assistant, persistent records, and mobile delivery. The implementation also needed to reuse working services instead of replacing them unnecessarily.

## Solution

Developed and tested small Python command-line modules and scheduled jobs integrating:

- A calendar interface that returns structured event data.
- SQLite-backed task records with completion history, recurring schedules, and archive/restore behavior.
- A self-hosted `ntfy` notification service and authenticated HTTP publishing to mobile clients.
- Existing Linux services, remote access, and independent AI assistant sessions.
- Human review and explicit deployment controls for significant changes.

**Core technologies:** Python, SQLite, JSON, HTTP, Linux, systemd/cron, ntfy, SSH, Tailscale, Git-based documentation.

## Architecture (high level)

```text
AI assistant / command-line users
                |
        Python workflow modules
          /             \
Calendar and SQLite   Notification publisher
          \             /
        Scheduled workflow logic
                |
   Authenticated self-hosted ntfy
                |
     Authorized mobile recipients
```

*This diagram is intentionally conceptual. It is not a production network diagram, and it excludes private addresses, tokens, personal data, and sensitive configuration details.*

## Engineering approach

1. Inspected existing calendar, notification, and task interfaces before selecting the smallest reusable integration path.
2. Implemented and tested changes in isolated environments, preserving original data and working services.
3. Verified SQLite record preservation and independently executed create/read/edit/archive/restore workflows.
4. Tested authenticated notification publishing, phone delivery, scheduled behavior, and failure handling.
5. Recorded tests, issues, configuration changes, and acceptance status in tracked roadmaps.

## Verification and results

- The V1 roadmap documents a working self-hosted notification server and successful message delivery to two mobile devices over an existing private network route.
- The V2 roadmap marks the task management, scheduled notification, and interactive notification implementation phases **Fully Complete** and documents multiple isolated functional tests.
- Specific tests include record preservation, recurrence behavior, delivery confirmations, and workflow verification across separate assistant sessions.
- Final V2 acceptance is **not complete** in the latest provided tracked roadmap. This case study does not claim complete production hardening, external customer deployment, formal security certification, or broad scale testing.

## Issues and lessons learned

- One session initially encountered a SQLite read-only error; investigation traced the difference to runtime execution permissions. This reinforced the importance of diagnosing execution context before altering storage.
- User-facing notifications required testing of formatting and delivery—not merely observing successful HTTP requests.
- Shared operating-system identities introduced authorization and isolation limitations that require explicit documentation and care.

## Individual contribution and tooling

Project planning, system integration, diagnostics, testing, and acceptance tracking were independently directed by the project owner. Development included AI-assisted coding and review; this case study does not claim that all implementation code was written unaided.
