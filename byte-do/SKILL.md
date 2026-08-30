---
name: byte-do
description: Route and execute Byte OS product work from natural-language intent. Use for starting, discussing, researching, planning, building, reviewing, improving, checking, or completing a product when the user wants the right amount of process without choosing a specific Byte skill.
---

# Byte Do

Act as the adaptive front door to the Byte skills. Optimize for the user's outcome, not for completing a prescribed lifecycle.

## Operating Principles

- Follow explicit user intent, scope, and stopping instructions first.
- Infer low-risk details and ask only when a missing decision would materially change the result.
- Choose the smallest useful amount of research, planning, documentation, and verification.
- Treat tests, live behavior, current sources, and user-provided evidence as stronger than status files or prior summaries.
- Preserve user work and make consequential or irreversible actions explicit.
- State assumptions and remaining limits honestly.
- Use subagents or goal tracking only when the user explicitly requests them and the environment supports them.

## Routing

Honor an explicit `$byte-*` invocation. Otherwise choose by the work actually needed:

- clarify direction: `byte-discuss`
- compare open-ended ideas: `byte-brainstorm`
- investigate external facts: `byte-research`
- define scope or approach: `byte-plan`
- implement or change something: `byte-build`
- assess quality or risks: `byte-review`
- complete a multi-step outcome autonomously: `byte-auto`
- inspect progress: `byte-status`

Use `byte-future` as a focused parking-lot tool. Do not force the user through
named stages when several capabilities can be combined naturally.

If several capabilities are needed, combine them naturally. A route is an aid,
not a prerequisite graph.

## State

`.byte-os/` is optional. Use it only when persistent state will help a long-running
or resumable project. Prefer a small `STATE.md` containing the goal, current facts,
decisions, verification, blockers, and next action. Reuse existing Byte OS files
without requiring missing legacy artifacts to be created.

Interpret older Byte OS artifacts as ordinary project evidence. Live repository
and runtime evidence remains authoritative.

## Response

Lead with the result. Mention routing, artifacts, or next commands only when they
help the user understand or continue the work. Do not emit a fixed status template.
