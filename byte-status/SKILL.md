---
name: byte-status
description: Summarize Your ByteDance / Byte OS state, artifacts, OKRs, plan progress, current stage, blockers, and next recommended action. Use when the user asks for status, progress, current stage, what exists, what is missing, or where to continue.
---

# Byte Status

Status reports where the Your ByteDance project stands and what should happen next.

## Workflow

1. Check whether `.byte-os/` exists.
2. Read `STATUS.md` if present.
3. Inspect core artifacts:

```text
BYTE.md
OKRS.md
RESEARCH.md
COMPETITORS.md
USER_ASSUMPTIONS.md
DISCUSSION.md
PRODUCT_SPEC.md
UX_SPEC.md
TECH_SPEC.md
CODEBASE_MAP.md
HARNESS.md
ROADMAP.md
BUILD_LOG.md
DELIVERY.md
```

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

6. Identify next action:

- No `.byte-os/`: `byte-start`
- Stage is discussing or `DISCUSSION.md` exists but no specs: `byte-shape`
- Started but no specs: `byte-shape`
- Existing codebase but no harness: `byte-codebase-harness`
- Specs but no plans: `byte-plan`
- Plans incomplete: `byte-build`
- Build complete but no review: `byte-review`
- Review says iterate or block: `byte-iterate`
- Review says ship: `byte-deliver`
- Real feedback provided: `byte-users`

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
Discussion:
Harness:
Subagents:
Blockers:
Next:
```

Do not modify files unless `STATUS.md` is missing or stale and the user asked to repair status. If repairing, update only `.byte-os/STATUS.md`.

## Completion Criteria

The user should know what has been done, what is missing, and the exact next Byte OS command.
