---
name: byte-do
description: Route natural-language product work to the right Your ByteDance / Byte OS skill and execute the matching workflow. Use when the user asks to start, continue, research, shape, plan, build, review, iterate, inspect status, analyze real users, auto-complete, or deliver a product using a ByteDance-inspired product squad.
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
  CODEBASE_MAP.md
  HARNESS.md
  ROADMAP.md
  DELIVERY.md
  plans/
  reviews/
  iterations/
  users/
  subagents/
```

If the directory does not exist, only `byte-start`, `byte-auto`, or a status explanation can proceed.

## Routing

Apply the first strong match:

| User intent | Route |
|---|---|
| "one click", "auto", "do it all", "from idea to delivery", "all tasks", "don't stop until done", "goal-like execution", "一键完成", "所有任务", "不完成不停" | `byte-auto` |
| "start", "new product", "from zero", no `.byte-os/` | `byte-start` |
| "research", "competitors", "benchmark", "pricing", "market" | `byte-research` |
| "shape", "MVP", "positioning", "scope", "flows", "design product" | `byte-shape` |
| "large codebase", "monorepo", "CLAUDE.md", "AGENTS.md", "codebase map", "harness", "LSP", "Claude and Codex", "noise filters" | `byte-codebase-harness` |
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

## Execution Rule

After routing, execute the selected workflow. If the selected skill body is available in the environment, follow it. If it is not available, use this fallback:

- `byte-start`: create `.byte-os/` and write project foundation files, including visible OKRs.
- `byte-research`: browse current sources for market and competitor facts, cite links, write `RESEARCH.md` and `COMPETITORS.md`.
- `byte-shape`: write product, UX, technical, and roadmap specs.
- `byte-codebase-harness`: create Claude/Codex context files, codebase map, scoped command matrix, noise filters, and harness status.
- `byte-plan`: create dependency-aware plan files under `.byte-os/plans/`.
- `byte-build`: execute the next dependency-ready plan wave, or the requested `--plan`, `--wave`, or `--all`.
- `byte-code-rules`: apply simple, surgical, verifiable engineering behavior rules.
- `byte-review`: run a cross-functional review and write `.byte-os/reviews/review-N.md`.
- `byte-users`: analyze only real feedback evidence; never simulate real users.
- `byte-iterate`: run structured improvement loops and write `.byte-os/iterations/iteration-N.md`.
- `byte-status`: summarize current state and next action.
- `byte-next`: infer and execute the next stage from `STATUS.md`.
- `byte-auto`: run start, research, shape, plan, build, review, at least 3 iteration loops, and deliver.
- `byte-deliver`: write final delivery summary, run instructions, verification, and remaining risks.

## Multi-Agent Policy

Byte OS is multi-role by design. Use actual subagents only when the user explicitly asks for multi-agent, parallel, team, or auto Byte OS execution and the platform allows it. Otherwise, emulate the project roles in one response and keep role output concise.

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
State: <new / existing / blocked>
Artifacts: <files created or updated>
Next: <next command or workflow>
```

Keep the final user-facing summary short, but make the files complete enough for the next Byte OS step.
