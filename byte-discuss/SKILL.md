---
name: byte-discuss
description: Discuss and clarify Your ByteDance / Byte OS product requirements before planning or building. Use when the user wants to brainstorm, discuss requirements, clarify an idea, ask what is unclear, confirm scope, compare product directions, or explicitly says not to write code yet.
---

# Byte Discuss

Discuss is the requirement-clarification mode. It helps the user turn a rough idea into confirmed product direction without starting implementation.

## Boundaries

- Do not write product code.
- Do not run `byte-auto`, `byte-build`, or implementation steps.
- Do not create final plans unless the user asks to move into `byte-plan`.
- You may create or update `.byte-os/DISCUSSION.md` to preserve the conversation, unless the user asks for discussion only with no files.
- If `.byte-os/` already exists, read current `BYTE.md`, `PRODUCT_SPEC.md`, `UX_SPEC.md`, `TECH_SPEC.md`, `OKRS.md`, and `STATUS.md` when present.

## Workflow

1. Restate the current understanding in 3-6 bullets.
2. Identify unclear or risky requirement areas.
3. Ask targeted questions automatically.
4. Offer reasonable default assumptions for low-risk gaps.
5. Confirm the next action: continue discussion, start, shape, plan, or auto.

## Question Rules

Ask only questions that affect product scope, UX, technical direction, business goal, delivery format, or acceptance criteria.

Use this priority order:

1. Target user and primary job to be done
2. Core problem and success outcome
3. MVP scope and non-goals
4. First user flow
5. Data, integrations, accounts, permissions, or external dependencies
6. Platform and delivery format
7. Quality bar, timeline, and constraints

Ask at most 7 questions per pass. Group them as:

```text
Must confirm:
Nice to confirm:
Suggested defaults:
```

If the user gives enough context, do not keep interrogating. Move to a confirmation summary and recommend the next Byte OS step.

## Discussion Output

Return:

```text
Current understanding:
Unclear points:
Questions:
Suggested defaults:
Confirmed scope:
Non-goals:
Risks:
Recommended next:
```

When writing state, create or update:

```text
.byte-os/DISCUSSION.md
.byte-os/STATUS.md
```

`DISCUSSION.md` should include:

- Date
- User request
- Current understanding
- Open questions
- Suggested defaults
- Confirmed decisions
- Non-goals
- Recommended next command

Update `STATUS.md`:

```text
Stage: discussing
Current command: byte-discuss
Next recommended command: byte-start or byte-shape
```

## Handoff

Recommend:

- `byte-start` when no Byte OS project exists and the user confirms the idea.
- `byte-shape` when the idea is clear enough to become specs.
- `byte-plan` when specs already exist and only execution breakdown remains.
- `byte-auto` only when the user explicitly wants one-click completion.

## Completion Criteria

Discuss is complete when the user has a concise confirmation checklist and the next Byte OS command is clear.
