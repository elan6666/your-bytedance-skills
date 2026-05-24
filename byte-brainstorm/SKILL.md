---
name: byte-brainstorm
description: Explicit-only Your ByteDance idea expansion mode. Use only when the user directly invokes `$byte-brainstorm` or explicitly asks to use byte-brainstorm. Expands rough ideas into multiple product directions, feature concepts, positioning angles, business models, and bold alternatives without entering the normal Byte OS workflow.
---

# Byte Brainstorm

Brainstorm is an explicit-only ideation mode. It expands possibilities before the user chooses what should become a real Byte OS project.

## Trigger Boundary

- Use only when the user explicitly invokes `$byte-brainstorm` or says to use `byte-brainstorm`.
- Do not let `byte-do`, `byte-auto`, `byte-next`, or the normal workflow call this automatically.
- Do not write product code.
- Do not create implementation plans.
- Do not start `byte-auto`.
- Do not turn ideas into committed scope unless the user chooses one.
- Do not update `.byte-os/STATUS.md` unless the user asks to save the brainstorm.

## Workflow

1. Capture the seed idea.
2. Generate several distinct directions, not small variations of the same idea.
3. For each direction, explain the user, core value, why it might work, and biggest risk.
4. Include both practical and high-upside options.
5. End with a decision menu and recommended next command.

## Brainstorm Lenses

Use the lenses that fit the idea:

- Conservative MVP
- Viral or shareable version
- Paid/professional version
- Community or creator version
- Data/network-effects version
- AI-native version
- Internal tool version
- Mobile-first version
- Browser/extension/plugin version
- Contrarian or high-risk version

## Output Format

Return:

```text
Seed idea:

Directions:
1. <direction name>
   - Target user:
   - Core value:
   - MVP shape:
   - Differentiator:
   - Risk:
   - Why now:

Best bets:

Questions before choosing:

Recommended next:
```

If the user asks for quantity, honor it. Otherwise produce 6-10 directions.

## Optional Save

If the user asks to save the brainstorm, write:

```text
.byte-os/BRAINSTORM.md
```

Do not treat saved brainstorms as confirmed scope. Mark them as options until the user chooses one.

## Handoff

Recommend:

- `$byte-discuss` when the user wants to clarify one direction.
- `$byte-start` when the user chooses a direction and wants to create a Byte OS project.
- `$byte-shape` when a project exists and the chosen direction should become specs.
- `$byte-auto` only when the user explicitly wants one-click execution.

## Completion Criteria

Brainstorm is complete when the user has multiple meaningfully different directions and a clear next step for choosing one.
