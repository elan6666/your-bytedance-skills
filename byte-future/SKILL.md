---
name: byte-future
description: Record deferred Your ByteDance / Byte OS ideas that are explicitly not part of current execution. Use when the user says to save something for later, future plan, someday, parking lot, not now, 以后做, 未来计划, 先记下来, 暂时不做, or 下个阶段再考虑. Never turn parked items into plans, code, review blockers, auto-mode work, or delivery requirements unless the user explicitly promotes one.
---

# Byte Future

Future is the non-blocking parking lot for ideas the user explicitly does not
want to execute now.

## Hard Boundary

- Record only; do not research, shape, plan, build, review, or implement.
- Write only `.byte-os/FUTURE.md`. Do not change `STATUS.md`, `OKRS.md`,
  `ROADMAP.md`, specs, plans, reviews, iterations, or delivery artifacts.
- Parked items are outside the current Objective, scope, plan waves, completion
  percentage, review verdict, iteration loop, Auto goal, and delivery gaps.
- `byte-auto`, `byte-next`, `byte-plan`, `byte-build`, `byte-review`, and
  `byte-iterate` must ignore parked items.
- Do not add a deadline, priority, owner, commitment, or success metric unless
  the user explicitly provides it.
- A future item can enter active work only after the user explicitly asks to
  promote or activate its `FTR-*` id.

If `.byte-os/` does not exist, create only the directory and `FUTURE.md`. This
does not initialize an active Byte OS project.

## Workflow

1. Read `.byte-os/FUTURE.md` when it exists.
2. Capture the user's idea without expanding its scope.
3. Assign the next stable id: `FTR-001`, `FTR-002`, and so on.
4. Record why it is deferred and what explicit trigger would justify revisiting
   it. Use `not specified` rather than inventing missing details.
5. Confirm that the current workflow and completion state are unchanged.

## Artifact Format

```markdown
# Future Plans

> Parked, non-blocking ideas. These are excluded from current Byte OS execution
> and Auto completion until explicitly promoted by the user.

## FTR-001 — <short title>

- Status: parked
- Recorded: <ISO-8601 date>
- Source: <user request or artifact>
- Why later: <reason or not specified>
- Revisit trigger: <explicit condition or not specified>
- Potential value: <brief note or not specified>
- Dependencies or unknowns: <brief note or not specified>
- Notes: <optional>
```

Allowed statuses are `parked`, `promoted`, and `rejected`. Only `parked` items
are future ideas; `promoted` items must link to the decision or active workflow
that accepted them.

## Promotion

Promotion requires explicit user language such as `promote FTR-003`,
`activate FTR-003`, or `现在开始做 FTR-003`.

When promotion is requested:

1. Mark the item `promoted` and record the date.
2. Route it through `byte-discuss`, `byte-research`, or `byte-shape` as needed.
3. Do not silently implement it inside `byte-future`.

## Output

```text
Recorded: FTR-<id> — <title>
Status: parked, non-blocking
Current workflow changed: no
Tracked by byte-auto: no
Artifact: .byte-os/FUTURE.md
```

## Completion Criteria

The idea is recorded faithfully, clearly marked as deferred, and excluded from
all current execution and completion tracking.
