---
name: byte-build
description: Execute Your ByteDance / Byte OS plan files by dependency-ready waves. Use when the user asks to build, implement, execute plans, run the next wave, run `byte-build --wave N`, run `byte-build --plan ID`, or run `byte-build --all`.
---

# Byte Build

Build executes plans. By default, it executes the next dependency-ready wave, not simply plan 001.

## Inputs

Read:

```text
.byte-os/STATUS.md
.byte-os/plans/*.plan.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/OKRS.md
.byte-os/CODEBASE_MAP.md
.byte-os/HARNESS.md
.byte-os/AGENTS_AUDIT.md
AGENTS.md and relevant module AGENTS.md files
```

If no plans exist, run or recommend `byte-plan`.

## Modes

```text
byte-build
```

Execute the next wave whose dependencies are complete.

```text
byte-build --wave N
```

Execute all ready plans in wave `N`.

```text
byte-build --plan ID
```

Execute one plan only.

```text
byte-build --all
```

Execute all waves until plans complete or a blocker appears.

In `byte-auto`, `byte-build --all` is not allowed to be the final stop unless all plans are complete or a hard blocker has been recorded. If a plan is blocked because it is underspecified, missing a scoped command, or needs repair after a failed check, return control to `byte-auto` with the exact repair action so auto mode can re-plan, fix, and retry.

## Execution Rules

- Inspect the repository before editing.
- For existing codebases, read the relevant `AGENTS.md`, `CLAUDE.md`, `.byte-os/CODEBASE_MAP.md`, `.byte-os/HARNESS.md`, and `.byte-os/AGENTS_AUDIT.md` before editing.
- Before editing a plan, build the context stack from the plan's `agents_context_stack` or by walking from `start_directory` up to repo root and reading applicable `AGENTS.md` files.
- If `AGENTS.md` is missing, bloated, stale, or lacks scoped commands for the touched area, record the gap and run or recommend `byte-codebase-harness` before broad edits.
- Start from the plan's `start_directory` or the most relevant module directory instead of always working from repo root.
- Apply `byte-code-rules` for all coding work: think before coding, keep the implementation simple, make surgical changes, and verify against explicit success criteria.
- Never revert user changes.
- Keep each plan's write scope clear.
- Use actual worker subagents only when explicitly authorized by the user or auto workflow; assign disjoint ownership from the plan's `Subagent Plan`.
- Prefer read-only exploration subagents for unfamiliar code before editing.
- Use implementation subagents only for steps marked `implementation_allowed` with explicit files, non-goals, acceptance criteria, and verification.
- Use review subagents after implementation to independently check acceptance criteria, regressions, and missed scoped commands.
- If subagents are not authorized or unavailable, execute locally but still preserve role ownership and exploration summaries in plan logs.
- Mark a plan `in_progress` before work and `complete` only after verification.
- Mark `blocked` with a clear reason when execution cannot continue.
- In auto mode, distinguish hard blockers from fixable blockers. Fixable blockers should feed back into planning, repair, iteration, or another `byte-build --all` pass.
- Run the most relevant tests, linters, type checks, builds, or manual verification available.
- Prefer scoped commands recorded in the plan or module context files over full-repo commands.
- Avoid generated files, dependency folders, vendored code, build outputs, and large artifacts unless the plan explicitly targets them.
- Use LSP or symbol-aware navigation when available for common names or large typed codebases; otherwise use `rg` and direct file reads.
- For frontend apps, start the dev server when appropriate and provide the URL after successful implementation.
- Keep a candid build log: what worked, what failed, what changed, and which Key Results moved.
- Log every subagent used, its scope, output artifact, files changed, verification, and handoff notes.
- Log which `AGENTS.md` files were read and which scoped commands came from them.

## Wave Selection

A plan is ready when:

- status is `pending` or `ready`
- all `depends_on` plans are `complete`
- no blocker is recorded

When multiple plans are ready in the same wave, execute in parallel only if subagent use is explicitly authorized and write scopes do not overlap.

## Subagent Execution

For each ready plan:

1. Read `Subagent Plan`.
2. Run read-only exploration first when the subsystem is unfamiliar.
3. Assign implementation subagents only to non-overlapping scopes.
4. Require each subagent to return:

```text
Scope:
Files inspected:
Files changed:
Verification run:
Result:
Risks:
Handoff:
```

5. Main agent reviews diffs and verification before marking the plan complete.

Never let two subagents edit the same file unless the plan explicitly defines sequencing and merge ownership.

## Artifacts

Update:

```text
.byte-os/plans/*.plan.md
.byte-os/STATUS.md
.byte-os/BUILD_LOG.md
```

`BUILD_LOG.md` should include:

- Date
- Mode
- Plans executed
- Files changed
- Code rule notes: assumptions, scope decisions, and any intentional tradeoffs
- Verification run
- Subagents used and handoffs
- AGENTS.md context stack used
- AGENTS.md gaps or proposed updates
- OKR or metric impact
- Failures or blockers
- Next wave

Update `STATUS.md`:

```text
Stage: building
Current wave: <N>
Plans complete: <X>/<Y>
Next recommended command: byte-build or byte-review
```

## Completion Criteria

Build is complete when every v0 plan is complete and the product can be reviewed as a working deliverable or faithful prototype.

In auto mode, partial wave completion is progress, not completion. Continue until every required plan is `complete`, or write a hard blocker with the blocked plan, reason, attempted fix, and exact user action required.
