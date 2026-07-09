---
name: byte-auto
description: Run Your ByteDance / Byte OS from idea to deliverable Byte Automatically. Use when the user asks for one-click completion, end-to-end Byte Delivery, auto mode, "do all steps", "don't stop until done", or to go from discussion to a shippable product with a ByteDance-inspired project team and evidence-led automatic iteration loops.
---

# Byte Auto

Auto runs the same stages as step-by-step mode, but continues without waiting after each stage. It does not skip planning, building, review, or iteration.

## Auto Goal Contract

`byte-auto` is a goal runner, not a single-step planner.

When auto mode starts, keep executing until the terminal goal is reached:

```text
all required plans complete
latest review is ship or user-accepted
delivery artifact exists
verification is recorded
```

Do not stop just because one plan, one wave, or one iteration finished. Do not end with only "next command" while there are incomplete plans, unresolved review findings, or missing delivery artifacts.

Only pause for a hard blocker:

- Missing credentials, account access, payment, hardware, or private data.
- Destructive operation that requires explicit user approval.
- Ambiguous product decision where a wrong choice would materially change the outcome.
- Safety, legal, or policy issue.
- Runtime/context limit. In this case, write the exact resume state and next action into `.byte-os/AUTO_RUN.md` and `.byte-os/STATUS.md`.

A normal implementation failure, failing test, missing file, incomplete plan, or review finding is not a reason to stop. Treat it as work to repair, re-plan, build, or iterate.

## Required Inputs

Collect or infer:

- Product idea
- Target user
- Delivery format
- Constraints
- Iteration count or completion gates

Ask only for the product idea if it is missing. If iteration count is missing,
default to 3. Respect an explicit positive iteration count; do not silently
replace the user's count. Regardless of count, verification and review gates
must still pass before delivery.

## End-to-End Flow

Run:

```text
enable Pursue Goal mode
sync project goal
decide Subagent mode
byte-start
byte-research when external market evidence is relevant or missing
byte-codebase-harness if working in an existing repo or large codebase
byte-shape
byte-plan
byte-build --all with safe parallel subagent execution when available
byte-review
byte-iterate x N, stopping early only when the requested count is complete and review gates pass
byte-review
byte-deliver
```

Where:

```text
N = user_requested_iterations when explicitly provided, otherwise 3
```

If the project already has `.byte-os/`, resume from the earliest incomplete stage.

If the work happens inside an existing repository, monorepo, legacy codebase, or multi-service system, run `byte-codebase-harness` before planning or building so Claude and Codex both get navigable context.

## Auto Completion Loop

After every stage, run the installed `byte-do` skill's shared resolver with
`python3 <byte-do-skill>/scripts/byte_state.py next --root <project-root>`.
Execute that workflow unless an Auto-specific gate below takes precedence:

1. If current external research is required and missing or stale, run
   `byte-research` before shaping irreversible market-dependent decisions.
2. If independent tracks are safe, use subagent mode, then merge and verify.
3. If a plan is fixably blocked or underspecified, repair or re-plan it rather
   than stopping.
4. If fewer than the requested/default iterations have run after a current
   review, run the next evidence-led iteration and then require a fresh review.
5. If verification is missing or stale, run focused verification and update the
   build and delivery records.
6. Stop only when the terminal contract is satisfied or a hard blocker exists.

Do not duplicate the lifecycle table here. Any change to routing order must be
implemented in the shared state contract, helper, and behavior tests.

Auto mode must repeat this loop until terminal completion or a hard blocker. The user should not need to manually type `byte-next`, `byte-build`, or `byte-review` during a normal auto run.

Track the run in:

```text
.byte-os/AUTO_RUN.md
```

Include:

- Goal
- Started at
- Current loop number
- Completed stages
- Remaining plans
- Review verdict
- Iteration count
- Subagent mode and active subagent scopes
- Hard blockers, if any
- Exact resume action

## Goal Integration

At the beginning of auto mode, turn on and use Codex's **Pursue Goal** mode for the project.

In the Codex composer UI, this is the `追求目标` toggle in the attachment/plus menu. If the UI is available and the toggle is off, ask the user to turn it on before continuing:

```text
Open the plus menu, enable 追求目标, then continue byte-auto.
```

If the Codex CLI is available, you may also check that the underlying goals feature exists:

```text
codex features list
```

If `goals` is present but disabled and the CLI supports enabling it, enable it:

```text
codex features enable goals
```

Do not claim that Pursue Goal mode has been enabled unless the UI/tool state confirms it. If the toggle cannot be controlled directly, ask the user to enable it and then continue. Do not block auto mode if the feature is already enabled or the environment has no goal UI.

Then create, refresh, or propose a single Codex goal for the project.

Use this goal to track the end-to-end outcome:

```text
Deliver <product idea> for <target user> as <delivery format>, with Byte OS planning, build, review, evidence-led iteration loops, and final handoff.
```

If the environment provides a way to create or update Codex goals, use it. If only the user-facing slash command is available, do not claim to have executed it. Instead, show the exact command for the user to run before continuing:

```text
/goal Deliver <product idea> for <target user> as <delivery format>, with Byte OS planning, build, review, evidence-led iteration loops, and final handoff.
```

After the goal is created or proposed, mirror the same objective in `.byte-os/STATUS.md` and `.byte-os/OKRS.md` so Byte OS can continue even if the goal feature is unavailable.

## Subagent Mode

`byte-auto` may use actual subagents automatically because auto mode is an end-to-end execution authorization. This does not authorize destructive actions, credential use, paid operations, or unsafe external side effects.

Set `Subagent mode` to `on` when the current work has safe parallel boundaries:

- Multiple ready plans in the same wave with no overlapping file or directory ownership.
- Independent tracks such as research, product shaping, UX, engineering, QA, growth, or delivery documentation.
- Large or unfamiliar codebases where read-only exploration can be split by subsystem.
- Implementation steps marked `implementation_allowed` with explicit files, non-goals, acceptance criteria, and verification.
- Review work that can be split by area, such as acceptance criteria, UI, tests, security, performance, or delivery readiness.

Set `Subagent mode` to `off` when the work is small, sequential, ambiguous, destructive, sensitive, or has overlapping write scopes.

Set `Subagent mode` to `unavailable` when actual subagents are useful but the platform cannot start them. In that case, keep the same task split in the plan and execute sequentially.

When subagent mode is `on`:

1. Create or update `.byte-os/SUBAGENTS.md` with the current subagent strategy.
2. Start read-only exploration subagents before implementation when context is uncertain.
3. Assign implementation subagents only to disjoint scopes and require a handoff.
4. Assign review subagents after implementation or after each completed wave.
5. Merge results through the main agent, run verification, and record the outcome in `.byte-os/BUILD_LOG.md`, `.byte-os/AUTO_RUN.md`, and `.byte-os/subagents/*.md`.

Every subagent handoff must include:

```text
Scope:
Allowed files or directories:
Files inspected:
Files changed:
Verification run:
Result:
Risks:
Handoff:
```

Never mark auto complete because subagents finished their slice. Auto completes only when the Auto Goal Contract is satisfied.

## Auto Mode Rules

- Use `.byte-os/STATUS.md` as the source of truth.
- Use `.byte-os/AUTO_RUN.md` as the auto-run ledger.
- Use `.byte-os/SUBAGENTS.md` as the subagent strategy and run ledger when subagents are used or considered.
- Use `.byte-os/OKRS.md` to keep work aligned to visible objectives and measurable key results.
- Preserve every artifact the step-by-step mode would create.
- Keep looping until the Auto Goal Contract is satisfied.
- Never treat "next recommended command" as the final answer in auto mode; execute it unless a hard blocker applies.
- Do not rely on simulated real users.
- Use `byte-users` only if real feedback evidence is provided.
- Use current web search for modern competitor, pricing, or trend claims.
- Apply `byte-code-rules` whenever auto mode plans, writes, reviews, or iterates on code.
- Use actual subagents when Subagent mode is `on` and the platform allows it; otherwise preserve the task split and run sequentially.
- Stop only for hard blockers that cannot be safely inferred or repaired.
- Be candid in logs: record weak assumptions, failed checks, and tradeoffs instead of hiding them.

## Iteration Focus

Default focus when the user does not specify a loop count:

1. Core completeness iteration
2. UX and onboarding iteration
3. Quality and delivery readiness iteration

Additional loops:

4. Differentiation and market iteration
5. Growth and monetization iteration

## Artifacts

Ensure core artifacts exist by the end:

```text
.byte-os/BYTE.md
.byte-os/OKRS.md
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/USER_ASSUMPTIONS.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/AUTO_RUN.md
.byte-os/ROADMAP.md
.byte-os/plans/*.plan.md
.byte-os/BUILD_LOG.md
.byte-os/reviews/review-*.md
.byte-os/iterations/iteration-*.md
.byte-os/DELIVERY.md
```

Conditional artifacts:

- Require `CODEBASE_MAP.md`, `HARNESS.md`, and `AGENTS_AUDIT.md` only for an
  existing codebase that needs a harness.
- Require `SUBAGENTS.md` and `subagents/*.md` only when subagents were used or a
  concrete subagent strategy was evaluated and recorded.

## Completion Criteria

Auto is complete only when every required plan is complete, the deliverable
exists, verification is recorded, the requested/default iteration count is
complete or a hard blocker is recorded, the latest review is current and
`ship` or user-accepted, and `DELIVERY.md` explains how to use, test, and
continue the product.
