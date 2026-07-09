---
name: byte-iterate
description: Run structured Your ByteDance / Byte OS iteration loops based on review findings, real user feedback, market research, test failures, metrics, experiments, or product goals. Use when the user asks to improve, optimize, iterate, create the next version, or run multiple automatic iterations.
---

# Byte Iterate

Iterate turns evidence into product improvements. In auto mode it defaults to 3
loops unless the user specifies a positive count. In manual mode it runs the
requested number, or 1 loop if unspecified.

## Inputs

Read available evidence:

```text
.byte-os/reviews/*.md
.byte-os/users/*.md
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/BUILD_LOG.md
.byte-os/ROADMAP.md
.byte-os/PRODUCT_SPEC.md
.byte-os/OKRS.md
```

Real user feedback must come from `byte-users` or user-provided materials. If none exists, label the iteration as based on internal review and research, not real users.

## Iteration Loop

For each loop:

1. Select evidence:
   - Review findings
   - Test failures
   - Real user feedback if available
   - Market or competitor changes if researched

2. Diagnose:
   - Product issue
   - UX issue
   - Technical issue
   - Growth issue
   - Quality issue

3. Prioritize:
   - Must fix
   - High leverage
   - Defer
   - Reject

4. Experiment:
   - Write the hypothesis.
   - Define metric, baseline, expected movement, and confidence.
   - Use A/B testing only when there is enough traffic and a measurable outcome.
   - Use usability tests, dogfooding, or instrumentation when A/B testing is not suitable.

5. Plan:
   - Create or update plan files for the iteration.
   - Keep scope small enough to execute.

6. Execute:
   - Use `byte-build` behavior for plan execution.
   - Apply `byte-code-rules` to keep iteration changes simple, scoped, and verifiable.
   - Run relevant verification.

7. Review:
   - Record before and after.
   - Decide whether another loop is needed.

## Auto Iteration Count

If invoked by `byte-auto`, use:

```text
iteration_count = user_requested_count if explicitly provided, otherwise 3
```

Respect an explicit positive count. Loop count never replaces the completion
gates: each executed loop still needs evidence, verification, and a fresh review
before delivery.

Suggested automatic loop focus:

- Iteration 1: completeness and core workflow
- Iteration 2: UX, onboarding, copy, error states
- Iteration 3: quality, tests, delivery readiness
- Iteration 4: differentiation and competitor response
- Iteration 5: growth, retention, monetization

## Artifacts

Write:

```text
.byte-os/iterations/iteration-N.md
```

Add frontmatter with `created_at`, the evidence source, and the originating
review when applicable. This lets the shared state resolver distinguish a new
iteration from the review that requested it.

Include:

- Evidence used
- Hypothesis and metric
- Diagnosis
- Changes planned
- Changes made
- Verification
- Remaining issues
- Next decision

Update:

```text
.byte-os/ROADMAP.md
.byte-os/STATUS.md
```

Update `STATUS.md` using the shared Byte OS state contract with
`stage: iterating`, `current_workflow: byte-iterate`, the new
`iteration_count`, and `next_workflow: byte-review`.

## Completion Criteria

An iteration is complete when changes are made or explicitly deferred, verification is recorded, and the next action is clear.
