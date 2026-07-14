# Byte OS State Contract

Use this contract whenever a Byte skill reads, routes, or updates `.byte-os/` state.
The deterministic helper is `scripts/byte_state.py` inside the installed
`byte-do` skill. Prefer it over reimplementing routing tables in individual
skills.

## Status Schema

`STATUS.md` remains human-readable Markdown. New writes should put stable routing
fields in YAML frontmatter:

```yaml
---
schema_version: 1
mode: step
project_kind: greenfield
stage: started
current_workflow: byte-start
next_workflow: byte-shape
review_verdict: none
iteration_count: 0
harness_status: not_required
hard_blocked: false
updated_at: 2026-01-01T00:00:00Z
---
```

Allowed values:

- `mode`: `step` or `auto`
- `project_kind`: `greenfield`, `existing_codebase`, or `unknown`
- `stage`: `discussing`, `started`, `researched`, `shaped`, `planned`,
  `building`, `reviewed`, `iterating`, `delivered`, or `blocked`
- `review_verdict`: `none`, `ship`, `iterate`, or `block`
- `harness_status`: `not_required`, `required`, `partial`, `ready`, or `blocked`
- `hard_blocked`: `true` only when progress requires user input or an external
  state change; ordinary test failures and repairable plan gaps are not hard blockers

Do not infer `existing_codebase` merely because `.git/` exists. A greenfield
project commonly initializes Git before Byte OS starts. Record the value during
`byte-start` or set it when repository evidence makes the distinction clear.

## Plan And Event Schema

Plan frontmatter keeps these stable fields:

```yaml
id: "001"
status: pending
wave: 1
depends_on: []
updated_at: 2026-01-01T00:00:00Z
```

Allowed plan statuses are `pending`, `ready`, `in_progress`, `complete`, and
`blocked`. A blocked plan should also record whether its blocker is fixable or
hard and the exact next action.

Review and iteration files should include `created_at` in frontmatter. The state
helper uses timestamps when present and file modification time as a legacy
fallback. An iteration or completed-plan update newer than the latest review
means the next workflow is `byte-review`, even if the older review said
`iterate` or `block`.

## Future Exclusion Contract

`.byte-os/FUTURE.md` is a parking lot, not active state.

- Parked `FTR-*` items do not belong to the current Objective, specs, roadmap
  scope, plans, waves, completion percentage, review findings, iteration input,
  Auto goal, delivery gaps, or next-workflow resolution.
- The existence, count, age, or content of parked items must never keep
  `byte-auto` running or change a `ship` verdict.
- `byte-status` may report parked/promoted/rejected counts for visibility, but
  its next action comes from active state only.
- When `FUTURE.md` is the only Byte OS artifact, route to `byte-status`; do not
  initialize, shape, or build a product from parked ideas.
- Only an explicit user request may mark an item `promoted`. Promotion then
  enters the normal workflow through discussion, research, or shaping.

## Canonical Routing Order

Apply the first matching rule:

1. Missing `.byte-os/` -> `byte-start`.
2. Only `FUTURE.md` exists -> `byte-status`; no active project has started.
3. A recorded hard blocker -> `byte-status` so the exact required user or
   external action is reported without retrying fixable workflows.
4. Unresolved brainstorm or discussion without specs -> `byte-discuss` or
   `byte-shape`.
5. `project_kind: existing_codebase` with an incomplete harness ->
   `byte-codebase-harness`.
6. Missing product, UX, or technical specs -> `byte-shape`.
7. Missing plans -> `byte-plan`.
8. Any incomplete plan -> `byte-build`.
9. Missing review, or build/iteration evidence newer than the latest review ->
   `byte-review`.
10. Latest current review is `iterate` or `block` -> `byte-iterate`.
11. Latest current review is `ship` and delivery is missing -> `byte-deliver`.
12. Delivery exists -> `byte-status`, unless the user explicitly supplies real
    user evidence and invokes `byte-users`.

Explicit user intent can select a safe workflow directly. It must not override
hard prerequisites, fabricate user evidence, or skip required verification.

## Helper Commands

Resolve the installed `byte-do` skill directory, then run:

```bash
python3 <byte-do-skill>/scripts/byte_state.py scan --root <project-root>
python3 <byte-do-skill>/scripts/byte_state.py next --root <project-root>
python3 <byte-do-skill>/scripts/byte_state.py validate --root <project-root>
python3 <byte-do-skill>/scripts/byte_state.py update --root <project-root> \
  --set stage=reviewed --set review_verdict=ship --set next_workflow=byte-deliver
```

If the helper is unavailable, follow this contract directly and record that
routing was inferred manually.
