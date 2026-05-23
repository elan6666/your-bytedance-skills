---
name: byte-auto
description: Run Your ByteDance / Byte OS from idea to deliverable Byte Automatically. Use when the user asks for one-click completion, end-to-end Byte Delivery, auto mode, "do all steps", or to go from discussion to a shippable product with a ByteDance-inspired project team and at least three automatic iteration loops.
---

# Byte Auto

Auto runs the same stages as step-by-step mode, but continues without waiting after each stage. It does not skip planning, building, review, or iteration.

## Required Inputs

Collect or infer:

- Product idea
- Target user
- Delivery format
- Constraints
- Iteration count

Ask only for the product idea if it is missing. If iteration count is missing, default to 3. If a count below 3 is provided, use 3.

## End-to-End Flow

Run:

```text
goal sync
byte-start
byte-shape
byte-plan
byte-build --all
byte-review
byte-iterate x N
byte-review
byte-deliver
```

Where:

```text
N = max(user_requested_iterations, 3)
```

If the project already has `.byte-os/`, resume from the earliest incomplete stage.

## Goal Integration

At the beginning of auto mode, create or refresh a single Codex goal for the project.

Use this goal to track the end-to-end outcome:

```text
Deliver <product idea> for <target user> as <delivery format>, with Byte OS planning, build, review, at least 3 iteration loops, and final handoff.
```

If the environment provides a way to create or update Codex goals, use it. If only the user-facing slash command is available, do not claim to have executed it. Instead, show the exact command for the user to run:

```text
/goal Deliver <product idea> for <target user> as <delivery format>, with Byte OS planning, build, review, at least 3 iteration loops, and final handoff.
```

After the goal is created or proposed, mirror the same objective in `.byte-os/STATUS.md` and `.byte-os/OKRS.md` so Byte OS can continue even if the goal feature is unavailable.

## Auto Mode Rules

- Use `.byte-os/STATUS.md` as the source of truth.
- Use `.byte-os/OKRS.md` to keep work aligned to visible objectives and measurable key results.
- Preserve every artifact the step-by-step mode would create.
- Do not rely on simulated real users.
- Use `byte-users` only if real feedback evidence is provided.
- Use current web search for modern competitor, pricing, or trend claims.
- Apply `byte-code-rules` whenever auto mode plans, writes, reviews, or iterates on code.
- Use actual subagents only when the user explicitly authorizes multi-agent or auto Byte OS execution and the platform allows it.
- Stop only for blockers that cannot be safely inferred.
- Be candid in logs: record weak assumptions, failed checks, and tradeoffs instead of hiding them.

## Iteration Focus

Run at least:

1. Core completeness iteration
2. UX and onboarding iteration
3. Quality and delivery readiness iteration

Additional loops:

4. Differentiation and market iteration
5. Growth and monetization iteration

## Artifacts

Ensure these exist by the end:

```text
.byte-os/BYTE.md
.byte-os/OKRS.md
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/USER_ASSUMPTIONS.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/ROADMAP.md
.byte-os/plans/*.plan.md
.byte-os/BUILD_LOG.md
.byte-os/reviews/review-*.md
.byte-os/iterations/iteration-*.md
.byte-os/DELIVERY.md
```

## Completion Criteria

Auto is complete when the deliverable exists, verification is recorded, at least 3 iterations have been run or explicitly blocked, and `DELIVERY.md` explains how to use, test, and continue the product.
