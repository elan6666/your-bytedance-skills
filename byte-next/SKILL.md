---
name: byte-next
description: Continue a Your ByteDance / Byte OS project by inferring and executing the next workflow step from `.byte-os/` state. Use when the user says next, continue, resume, proceed, or asks what to do after the current stage.
---

# Byte Next

Next advances the project one step. It is the step-by-step mode companion to `byte-auto`.

Do not use `byte-next` as a substitute for auto mode. If the user asks for one-click completion, all remaining tasks, "don't stop until done", or goal-like execution, route to `byte-auto` instead.

## Workflow

1. Inspect `.byte-os/`.
2. Read the installed `byte-do` skill's `references/state-contract.md`.
3. Run `python3 <byte-do-skill>/scripts/byte_state.py next --root
   <project-root>` when the helper is available. Otherwise apply the state
   contract manually.
4. Check `OKRS.md` so the next step advances visible goals.
5. Execute the workflow, not merely describe it, unless execution would be risky or requires missing input.
6. If the workflow writes, reviews, refactors, or iterates on code, apply `byte-code-rules`.
7. Update `STATUS.md`.

## State Resolution

The shared state resolver owns lifecycle ordering. In particular:

- Existing codebases must complete the harness before planning or building.
- An iteration or completed-plan update newer than the latest review routes to
  `byte-review`, even when the older review verdict was `iterate` or `block`.
- `byte-users` is selected only from explicit real user evidence, never merely
  because delivery exists.
- Parked items in `.byte-os/FUTURE.md` are informational only. They never
  select a lifecycle step, and `byte-next` must not promote them implicitly.
- A project containing only `FUTURE.md` routes to `byte-status`; it is not an
  initialized active project.

Do not copy the canonical routing table into this skill. Update the shared
contract and its behavior tests when lifecycle rules change.

## Safety

Ask one concise question if:

- The product idea is missing and no project exists.
- The next step would require destructive changes.
- Real user feedback is required but absent.
- The user asks for auto mode but iteration count or delivery target is unclear and the default would be risky.

Otherwise make reasonable assumptions and record them in `DECISIONS.md`.

## Output

Always report:

```text
Previous stage:
Selected next workflow:
Reason:
Artifacts updated:
Next command:
```

## Completion Criteria

The project has advanced exactly one major Byte OS step.
