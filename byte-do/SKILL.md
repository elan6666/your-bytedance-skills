---
name: byte-do
description: Route natural-language product work to the right Your ByteDance / Byte OS skill, decide whether goal mode or subagent mode is appropriate, and execute the matching workflow. Use when the user asks to start, discuss, continue, research, shape, plan, build, review, iterate, inspect status, analyze real users, auto-complete, parallelize, use subagents, or deliver a product using a ByteDance-inspired product squad.
---

# Byte Do

Byte Do is the front door for Your ByteDance. It reads the user's request and the `.byte-os/` byte state, chooses the correct Byte OS workflow, then executes that workflow instead of only naming it.

## Your ByteDance Operating Model

Run the project like a ByteDance-inspired product squad:

- Always Day 1: prefer speed, simplicity, and learning.
- Context, not control: make state, OKRs, decisions, evidence, blockers, and next actions visible in files.
- Candid and clear: expose problems directly and separate facts, assumptions, and opinions.
- Seek truth and be pragmatic: use current research, first-hand user evidence, tests, and measurable impact.
- Aim high with ROI: compare alternatives, take calculated risks, and avoid low-impact busywork.
- Experimentation culture: convert uncertain choices into hypotheses, metrics, tests, or iteration loops.
- Cross-functional execution: product, research, UX, engineering, QA, and growth work in parallel when dependencies allow.
- Engineering discipline: apply `byte-code-rules` when planning, writing, reviewing, refactoring, or iterating on code.

## Byte OS State

Use `.byte-os/` in the current project root:

```text
.byte-os/
  BYTE.md
  STATUS.md
  OKRS.md
  DECISIONS.md
  RESEARCH.md
  COMPETITORS.md
  USER_ASSUMPTIONS.md
  PRODUCT_SPEC.md
  UX_SPEC.md
  TECH_SPEC.md
  DISCUSSION.md
  BRAINSTORM.md
  AUTO_RUN.md
  CODEBASE_MAP.md
  HARNESS.md
  AGENTS_AUDIT.md
  ROADMAP.md
  DELIVERY.md
  plans/
  reviews/
  iterations/
  users/
  subagents/
```

If the directory does not exist, only `byte-brainstorm`, `byte-discuss`, `byte-start`, `byte-auto`, or a status explanation can proceed.

## Preflight

Before routing:

1. Detect explicit skill invocation.
   - If the user directly invokes `$byte-brainstorm` or explicitly says to use `byte-brainstorm`, route to `byte-brainstorm`.
   - Do not route ordinary "brainstorm", "idea", or "expand this" language to `byte-brainstorm`; use `byte-discuss` or `byte-shape` unless the user explicitly names the skill.
2. Inspect `.byte-os/` when present.
3. Read [references/state-contract.md](references/state-contract.md) for broad
   requests such as "continue", "what now", or "status". Run
   `scripts/byte_state.py next --root <project-root>` when the helper is
   available instead of reimplementing state routing.
4. Decide whether Codex **Pursue Goal** mode should be used.
5. Decide whether **Subagent mode** should be used.
6. Route and execute the workflow.

## Goal Mode Decision

Use goal mode when the request is a multi-step outcome that should continue across planning, building, review, iteration, or delivery.

Set `Goal mode` to `on` and turn on or create/sync a goal for:

- `byte-auto`
- "one click", "do it all", "don't stop until done", "all tasks", "from idea to delivery", "一键完成", "所有任务", "不完成不停"
- A request with an explicit deliverable plus multiple phases, such as design + build + test, or plan + implement + review
- Long-running project work where stopping after one step would be wrong
- Resuming an existing `.byte-os/` project whose next action spans multiple incomplete artifacts

Set `Goal mode` to `suggested` when the request is probably multi-step but the user did not clearly ask for continuous execution. In this case, explain why goal mode would help and continue with the safest current workflow unless the user confirms auto execution.

Set `Goal mode` to `off` for:

- `byte-brainstorm`
- `byte-discuss`
- `byte-status`
- Simple one-step research, review, explanation, or inspection
- Requests where the user explicitly says "just discuss", "only brainstorm", "don't write code", or "不要开始"

Set `Goal mode` to `unavailable` when goal mode is appropriate but cannot be enabled or confirmed in the current environment.

If goal mode should be used:

- If a goal API/tool is available, create or update one concise goal.
- If only the UI toggle is available, ask the user to enable `追求目标` before continuing.
- If goal mode cannot be controlled, mirror the goal into `.byte-os/STATUS.md` and `.byte-os/OKRS.md` and continue with the right workflow.

Goal template:

```text
Deliver <requested outcome> with Byte OS planning, execution, review, iteration, verification, and final handoff.
```

Do not claim goal mode is enabled unless the tool or UI state confirms it.

## Subagent Mode Decision

Use subagent mode to split exploration, implementation, review, QA, research, or product work across independent scopes when the platform supports actual subagents. Subagent mode is for parallel speed and context isolation, not for decorative role-play.

Set `Subagent mode` to `on` when at least one of these is true:

- The route is `byte-auto`.
- The user explicitly asks for "subagent", "subagents", "parallel agents", "multi-agent", "team execution", "并行", "子代理", or "多代理".
- Existing plans contain dependency-ready work with disjoint files, directories, services, screens, or artifacts.
- The request spans multiple independent tracks, such as research + UX + engineering + QA, or frontend + backend + data.
- A large or unfamiliar codebase needs read-only exploration across several subsystems before editing.
- A completed build needs independent review across acceptance criteria, regressions, UI, tests, and delivery readiness.

Set `Subagent mode` to `suggested` when the task looks parallelizable but actual subagent authorization or platform support is unclear. Continue with the safest single-agent workflow and include a recommended next action to enable subagents.

Set `Subagent mode` to `off` for:

- `byte-brainstorm`, `byte-discuss`, or `byte-status`
- Small, single-file, single-answer, or explanation-only tasks
- Tasks with overlapping write scopes that cannot be sequenced cleanly
- Unresolved product decisions where parallel implementation would amplify the wrong assumption
- Sensitive, destructive, credentialed, or externally irreversible actions

Set `Subagent mode` to `unavailable` when subagents would help but the current environment has no subagent tool or cannot run them safely.

When subagent mode is `on`:

- Prefer read-only exploration subagents first for unfamiliar areas.
- Assign implementation subagents only to disjoint file or directory scopes with explicit non-goals and verification.
- Assign review subagents after implementation, not during overlapping edits.
- The main agent keeps merge ownership, resolves conflicts, verifies outputs, and decides completion.
- Write or update `.byte-os/SUBAGENTS.md` and `.byte-os/subagents/*.md` with scope, files inspected or changed, verification, result, risks, and handoff.

Never let two subagents edit the same file unless a plan explicitly defines sequence and merge ownership.

## State-Aware Routing

Use explicit user intent first. If the user asks to start, discuss, research, review, auto-complete, or explicitly invokes `$byte-brainstorm`, honor that.

When intent is broad, such as "continue", "what now", "do the next thing",
"help me with this project", or "继续", use the canonical routing order in
`references/state-contract.md`. The state helper is authoritative when its
result is consistent with explicit user intent and safety constraints.

Do not maintain another routing table in this skill. If a new lifecycle state
is introduced, update the state contract, helper, and tests together.

## Routing

Apply the first strong match:

| User intent | Route |
|---|---|
| explicit `$byte-brainstorm` or explicit "use byte-brainstorm" | `byte-brainstorm` |
| "one click", "auto", "do it all", "from idea to delivery", "all tasks", "don't stop until done", "goal-like execution", "一键完成", "所有任务", "不完成不停" | `byte-auto` |
| "discuss", "clarify", "requirements discussion", "confirm scope", "unclear requirements", "don't write code yet", "讨论", "讨论需求", "先聊", "先别写代码", "确认需求", "不清楚的需求" | `byte-discuss` |
| "start", "new product", "from zero", no `.byte-os/` | `byte-start` |
| "research", "competitors", "benchmark", "pricing", "market" | `byte-research` |
| "shape", "MVP", "positioning", "scope", "flows", "design product" | `byte-shape` |
| "large codebase", "monorepo", "CLAUDE.md", "AGENTS.md", "agent.md", "Codex context", "codebase map", "harness", "LSP", "Claude and Codex", "noise filters" | `byte-codebase-harness` |
| "plan", "break down", "roadmap to tasks", "plans" | `byte-plan` |
| "build", "implement", "execute", "develop" | `byte-build` |
| "code rules", "coding guidelines", "engineering rules", "Karpathy" | `byte-code-rules` |
| "subagent", "subagents", "parallel agents", "exploration agent", "read-only agent" | `byte-codebase-harness` for exploration setup, or `byte-plan`/`byte-build` if plans already exist |
| "review", "audit", "check quality", "project meeting" | `byte-review` |
| "real users", "feedback", "user testing", "interview notes", "analytics" | `byte-users` |
| "iterate", "next version", "improve", "optimize" | `byte-iterate` |
| "status", "progress", "where are we" | `byte-status` |
| "next", "continue", "what should I do now" | `byte-next` |
| "deliver", "handoff", "final package", "ship" | `byte-deliver` |

If two routes are plausible, choose the route that advances the byte state. Ask one concise question only when choosing would be risky.

`byte-brainstorm` is explicit-only and outside the normal workflow. Only route to it when the user explicitly invoked `$byte-brainstorm` or explicitly asked to use `byte-brainstorm`.

## Execution Rule

After routing, execute the selected workflow. If the selected skill body is available in the environment, follow it. If it is not available, use this fallback:

- `byte-start`: create `.byte-os/` and write project foundation files, including visible OKRs.
- `byte-brainstorm`: expand a rough idea into multiple directions only when explicitly invoked; do not enter the normal workflow.
- `byte-discuss`: clarify requirements, ask targeted questions, suggest defaults, and optionally write `.byte-os/DISCUSSION.md` without writing product code.
- `byte-research`: browse current sources for market and competitor facts, cite links, write `RESEARCH.md` and `COMPETITORS.md`.
- `byte-shape`: write product, UX, technical, and roadmap specs.
- `byte-codebase-harness`: create Claude/Codex context files, root and module `AGENTS.md`, codebase map, scoped command matrix, noise filters, `AGENTS_AUDIT.md`, and harness status.
- `byte-plan`: create dependency-aware plan files under `.byte-os/plans/`.
- `byte-build`: execute the next dependency-ready plan wave, or the requested `--plan`, `--wave`, or `--all`.
- `byte-code-rules`: apply simple, surgical, verifiable engineering behavior rules.
- `byte-review`: run a cross-functional review and write `.byte-os/reviews/review-N.md`.
- `byte-users`: analyze only real feedback evidence; never simulate real users.
- `byte-iterate`: run structured improvement loops and write `.byte-os/iterations/iteration-N.md`.
- `byte-status`: summarize current state and next action.
- `byte-next`: resolve and execute the next stage using the shared state contract.
- `byte-auto`: run start, research, shape, plan, build, review, evidence-led iteration, and delivery; default to 3 iteration loops when the user does not specify a count.
- `byte-deliver`: write final delivery summary, run instructions, verification, and remaining risks.

## Recommended Next Menu

When the selected workflow is not `byte-auto`, end with a short menu of useful next actions. Keep it concrete and omit irrelevant options.

Examples:

```text
Recommended next:
1. Continue clarifying: $byte-discuss <topic>
2. Turn this into specs: $byte-shape
3. Run one-click execution: $byte-auto <confirmed goal>
```

For explicit brainstorm output, recommend `byte-discuss`, `byte-start`, or `byte-shape`, but not `byte-auto` unless the user asked for one-click execution.

For goal-mode candidates, include one option that enables or confirms `追求目标`.

## Multi-Agent Policy

Byte OS is multi-role by design. Use the Subagent Mode Decision above to decide whether actual subagents should run. If subagents are unavailable or unsafe for the current task, emulate the project roles in one response and keep role output concise.

Core roles:

- Product Director
- Product Manager
- Market Researcher
- UX Researcher
- Product Designer
- Tech Lead
- Frontend Engineer
- Backend Engineer
- QA Engineer
- Growth Analyst
- User Feedback Analyst

Each role must contribute evidence, decisions, or executable work. Avoid decorative role-play.

## Output

Always state:

```text
Routing: byte-*
Reason: <one sentence>
Goal mode: on | off | suggested | unavailable
Subagent mode: on | off | suggested | unavailable
State: <new / existing / blocked>
Artifacts: <files created or updated>
Next: <next command or workflow>
Recommended next:
1. <option>
2. <option>
```

Keep the final user-facing summary short, but make the files complete enough for the next Byte OS step.
