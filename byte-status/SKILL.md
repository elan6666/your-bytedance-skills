---
name: byte-status
description: Summarize Your ByteDance / Byte OS state, artifacts, OKRs, plan progress, current stage, blockers, and next recommended action. Use when the user asks for status, progress, current stage, what exists, what is missing, or where to continue.
---

# Byte Status

Status reports where the Your ByteDance project stands and what should happen next.

## Workflow

1. Check whether `.byte-os/` exists.
2. Read the installed `byte-do` skill's `references/state-contract.md`, then run
   `python3 <byte-do-skill>/scripts/byte_state.py scan --root <project-root>`
   and `python3 <byte-do-skill>/scripts/byte_state.py next --root
   <project-root>` when available.
   Treat helper output as the normalized view while still inspecting the human
   artifacts for meaning and blockers.
3. Inspect core artifacts:

```text
BYTE.md
OKRS.md
RESEARCH.md
COMPETITORS.md
USER_ASSUMPTIONS.md
BRAINSTORM.md
DISCUSSION.md
PRODUCT_SPEC.md
UX_SPEC.md
TECH_SPEC.md
CODEBASE_MAP.md
HARNESS.md
AGENTS_AUDIT.md
ROADMAP.md
BUILD_LOG.md
DELIVERY.md
FUTURE.md
```

Also check whether root `AGENTS.md` and relevant module `AGENTS.md` files exist when the project is an existing codebase.

4. Inspect directories:

```text
plans/
reviews/
iterations/
users/
subagents/
```

5. Count plan statuses:

```text
pending
ready
in_progress
complete
blocked
```

6. Identify the next action from the shared resolver. Do not maintain a separate
   lifecycle decision table here. Explicit real feedback may select
   `byte-users`; otherwise report the resolver result and reason.
7. If `FUTURE.md` exists, report parked, promoted, and rejected counts as
   informational data. Label parked items as excluded from active scope,
   blockers, completion, and next-step resolution.

## Output

Return:

```text
Stage:
Progress:
Objective:
Key Results:
Artifacts:
Plans:
Reviews:
Iterations:
Real user feedback:
Brainstorm:
Discussion:
Harness:
AGENTS.md:
Subagents:
Future plans: <counts; non-blocking and excluded>
Blockers:
Next:
```

Do not modify files unless `STATUS.md` is missing or stale and the user asked to repair status. If repairing, update only `.byte-os/STATUS.md`.

## Completion Criteria

The user should know what has been done, what is missing, and the exact next Byte OS command.
