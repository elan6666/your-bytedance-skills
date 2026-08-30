---
name: byte-build
description: Implement or change a product, codebase, document, prototype, or other deliverable and verify the result. Use when the user asks to build, execute, develop, fix, integrate, or carry out an existing plan.
---

# Byte Build

Implement the user's requested outcome with the smallest sound change set.

## Execution

1. Inspect the relevant files, instructions, and current behavior.
2. Read relevant active entries in `.byte-os/LESSONS.md` when present.
3. Identify the intended result and the most relevant verification.
4. Make focused changes while preserving unrelated user work.
5. Run proportionate tests, builds, checks, or direct inspection.
6. Repair important failures that are within scope.

Use an existing plan when helpful, but do not require Byte OS plans, OKRs,
harness files, waves, or role assignments before working. Adjust a stale plan
when live evidence shows a better route.

Prefer simple implementations and narrow diffs. Broaden the change only when the
goal or discovered architecture genuinely requires it. Avoid opportunistic
refactors that do not improve the requested result.

Use persistent logs only for long-running, risky, or resumable work. When state is
useful, record concise facts and verification rather than maintaining several
parallel ledgers.

Completion means the requested change is present and relevant verification has
passed, or any remaining verification limit is clearly disclosed.

When failed verification exposes a reusable false assumption or the user corrects
the intended behavior, update `.byte-os/LESSONS.md` with the confirmed mistake,
evidence, and prevention rule. Do not log every failed command or normal debugging
step.
