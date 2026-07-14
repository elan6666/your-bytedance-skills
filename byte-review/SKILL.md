---
name: byte-review
description: Run a cross-functional Your ByteDance / Byte OS project review. Use when the user asks to review, audit, critique, check quality, simulate a ByteDance-inspired product meeting, assess readiness, or find issues before delivery or iteration.
---

# Byte Review

Review is the internal project-team quality gate. It may use assumptions, specs, code, screenshots, and tests, but it must not pretend to be real user feedback.

## Inputs

Read available artifacts:

```text
.byte-os/BYTE.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/ROADMAP.md
.byte-os/OKRS.md
.byte-os/CODEBASE_MAP.md
.byte-os/HARNESS.md
.byte-os/AGENTS_AUDIT.md
.byte-os/plans/*.plan.md
.byte-os/BUILD_LOG.md
AGENTS.md and relevant module AGENTS.md files
```

Inspect the actual product or code when available.

Treat parked entries in `.byte-os/FUTURE.md` as outside the review baseline.
They cannot become findings, verification gaps, required changes, or verdict
blockers. A review may mention their count as non-blocking context only.

## Review Roles

- Product Director: strategic fit and decision quality.
- Product Manager: requirement completeness and priority.
- UX Researcher: user journey and friction.
- Product Designer: interface structure and interaction quality.
- Tech Lead: architecture and maintainability.
- QA Engineer: bugs, edge cases, missing tests.
- Growth Analyst: activation, retention, monetization.
- Market Researcher: competitor gap, only if current research exists or browsing is performed.

Use the Your ByteDance style: be candid and clear, ground conclusions in facts, and call out weak context instead of smoothing it over.

Use actual subagents only when explicitly authorized. Otherwise synthesize roles inline.

## Review Dimensions

Check:

- Does the product solve the stated problem?
- Is the MVP complete and focused?
- Is the first user workflow obvious?
- Are key states handled?
- Are acceptance criteria satisfied?
- Are tests or verification sufficient for the risk?
- Are security, privacy, data, or compliance risks present?
- Does the product have a reason to exist versus substitutes?
- Is it ready for delivery, or does it need iteration?
- Did the work advance the stated Objective or Key Results?
- Which assumptions need an experiment or real user evidence?
- Did coding work follow `byte-code-rules`: simple implementation, surgical diff, no unrelated refactors, explicit assumptions, and recorded verification?
- For existing codebases, did the work use the right `AGENTS.md`/`CLAUDE.md`, scoped commands, codebase map, noise filters, and start directory?
- Is root `AGENTS.md` lean, accurate, and pointer-oriented instead of becoming a long knowledge dump?
- Do module `AGENTS.md` files exist only where they reduce navigation cost?
- Are scoped commands, safe edit boundaries, generated/noisy paths, LSP hints, and subagent boundaries recorded for active areas?
- Does `.byte-os/AGENTS_AUDIT.md` contain a recent review date and proposed updates?
- If subagents were used, were their scopes isolated, factual, verified, and reviewed by the main agent before completion?

## Output

Write:

```text
.byte-os/reviews/review-N.md
```

Add frontmatter with `created_at` and `verdict`. A review is current only for
build and iteration evidence that existed when the review was created.

Include:

```text
# Verdict
ship | iterate | block

# Findings
Severity, owner role, evidence, recommended fix

# Role Notes
Concise notes by role

# Required Changes
Must fix before delivery

# Suggested Changes
Can improve after delivery

# Verification Gaps
Tests, checks, or user evidence still missing

# Engineering Rule Findings
Overengineering, broad unrelated edits, hidden assumptions, unverified success criteria, or cleanup risks

# Harness Findings
Missing or stale codebase maps, missing/bloated/stale AGENTS.md files, unscoped commands, noisy generated paths, weak LSP guidance, unsafe start directories, or missing AGENTS_AUDIT.md

# Subagent Findings
Scope overlap, unreviewed handoffs, missing verification, exploratory edits, or unclear ownership

# Decision
Next command
```

Update `STATUS.md` using the shared Byte OS state contract:

```text
stage: reviewed
current_workflow: byte-review
review_verdict: <ship|iterate|block>
next_workflow: <shared resolver result>
```

## Completion Criteria

Review is complete when there is a clear verdict, prioritized findings, and a next action.
Parked future entries do not affect the verdict or completion decision.
