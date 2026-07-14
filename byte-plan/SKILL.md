---
name: byte-plan
description: Convert Your ByteDance / Byte OS specs into dependency-aware executable plans. Use when the product has been shaped and needs multiple plan files for design, engineering, testing, launch, OKR execution, or when the user asks to break the product into project plans before building.
---

# Byte Plan

Plan splits shaped product work into small, executable plan files. Plans are the unit that `byte-build` executes.

## Inputs

Read:

```text
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/ROADMAP.md
.byte-os/OKRS.md
.byte-os/DECISIONS.md
.byte-os/CODEBASE_MAP.md
.byte-os/HARNESS.md
.byte-os/AGENTS_AUDIT.md
AGENTS.md and relevant module AGENTS.md files
```

If these are missing, run or recommend `byte-shape`.

## Planning Rules

- Create plans that can be executed independently when dependencies allow.
- Prefer wave-based parallelism over strict 1-to-N order.
- Keep write scopes clear to reduce conflicts.
- For engineering work, apply `byte-code-rules`: simple scope, surgical changes, explicit assumptions, and verifiable success criteria.
- Include acceptance criteria in every plan.
- Include verification steps in every plan.
- Connect every plan to at least one Objective or Key Result.
- Mark dependencies explicitly.
- Break every plan into explicit ordered steps: Step 1, Step 2, Step 3, etc.
- Each step must state what to do, why it is needed, touched files or modules, expected output, and how to verify that step.
- For existing codebases, use `.byte-os/CODEBASE_MAP.md` and `.byte-os/HARNESS.md` to choose the relevant start directory, applicable `CLAUDE.md`/`AGENTS.md`, and scoped commands.
- Build an `AGENTS.md` context stack for each plan: root `AGENTS.md`, then the nearest module `AGENTS.md` files that apply to `start_directory`.
- If a plan touches an area with no scoped command guidance in `AGENTS.md`, `CODEBASE_MAP.md`, or `HARNESS.md`, add a harness repair step before implementation.
- Prefer module-level test/lint/build commands over whole-repo commands when a plan touches one service or package.
- Mark whether each plan or step can be delegated to a subagent. Delegate only when scope, files, and verification are clear.
- Never pull parked entries from `.byte-os/FUTURE.md` into scope, dependencies,
  acceptance criteria, or verification. Only an explicitly promoted entry may
  enter planning through the normal discuss, research, or shape workflow.

## Plan File Format

Create files in `.byte-os/plans/`:

```markdown
---
id: 001
title: Foundation Setup
status: pending
wave: 1
updated_at: <ISO-8601 UTC timestamp>
owner_role: Tech Lead
depends_on: []
start_directory: .
context_files: [AGENTS.md, CLAUDE.md]
agents_context_stack: [AGENTS.md, <module>/AGENTS.md]
subagent_policy: none | read_only_exploration | implementation_allowed
---

# Goal

# OKR Link

# Scope

# Non-Goals

# Steps

## Step 1: <short action title>

- Purpose:
- Actions:
- Files or modules:
- Expected output:
- Step verification:
- Subagent: none | read_only_exploration | implementation_allowed

## Step 2: <short action title>

- Purpose:
- Actions:
- Files or modules:
- Expected output:
- Step verification:
- Subagent: none | read_only_exploration | implementation_allowed

# Dependencies

# Scoped Commands

- Test:
- Lint:
- Typecheck:
- Build:

# AGENTS.md Context

- Root context:
- Module context:
- Scoped command source:
- Safe edit boundaries:
- Missing or stale AGENTS.md notes:

# Subagent Plan

- Exploration subagents:
- Implementation subagents:
- Review subagents:
- Isolation boundaries:
- Merge or handoff notes:

# Code Change Guardrails

# Acceptance Criteria

# Verification

# Experiment Or Measurement

# Risks

# Notes
```

Status values:

```text
pending
ready
in_progress
complete
blocked
```

## Recommended Plan Set

Adapt to the product, but start from:

```text
001-foundation.plan.md
002-byte-core.plan.md
003-ux-shell.plan.md
004-frontend.plan.md
005-backend-or-data.plan.md
006-integration.plan.md
007-test-and-quality.plan.md
008-launch-and-delivery.plan.md
```

For a document-only or prototype-only deliverable, replace engineering plans with content, prototype, or validation plans.

## Wave Design

Assign wave numbers so `byte-build` can execute:

- Wave 1: foundation and scaffolding
- Wave 2: independent product surfaces or services
- Wave 3: integration and core workflow
- Wave 4: testing, quality, polish
- Wave 5: launch and delivery

Use the Your ByteDance style: plans should be transparent enough that another agent can execute with context, not control.

## Step Design

Plan files must be actionable step documents, not vague task lists.

Each step should be small enough to execute in one focused pass and concrete enough that `byte-build` can follow it without re-planning. Prefer this shape:

```markdown
## Step N: <verb + object>

- Purpose: <why this step exists>
- Actions:
  - <specific action>
  - <specific action>
- Files or modules:
  - <path or module>
- Expected output: <observable result>
- Step verification: <command, inspection, test, or manual check>
```

Use steps to decompose requirements, for example:

```markdown
## Step 1: Create the project shell
## Step 2: Build the primary user flow
## Step 3: Add persistence
## Step 4: Add empty, loading, and error states
## Step 5: Verify the workflow end to end
```

The `# Acceptance Criteria` section still describes the plan-level finish line. The `# Verification` section still describes the final checks for the whole plan.

## Subagent Design

Use subagents for parallelism and context isolation, not for vague outsourcing.

Good subagent tasks:

- Map one unfamiliar subsystem and write `.byte-os/subagents/exploration-<area>.md`.
- Implement one isolated module with explicit files and tests.
- Review one completed plan against acceptance criteria.

Avoid subagents when:

- The write scope overlaps heavily.
- Product decisions are unresolved.
- The task requires continuous cross-file judgment by the main agent.
- Verification cannot be scoped.

Every implementation subagent must have:

- Allowed files or directories
- Non-goals
- Acceptance criteria
- Verification command
- Handoff format

## Artifacts

Write or update:

```text
.byte-os/plans/*.plan.md
.byte-os/STATUS.md
.byte-os/ROADMAP.md
```

Update `STATUS.md` using the shared Byte OS state contract:

```text
stage: planned
current_workflow: byte-plan
next_workflow: byte-build
```

## Completion Criteria

The step is complete when every v0 requirement maps to at least one plan, every plan has acceptance criteria, and dependencies form executable waves.
