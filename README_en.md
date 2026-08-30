# Your ByteDance Skills

![Your ByteDance social preview](assets/social-preview.webp)

Your own product team, powered by Codex skills.

> Inspired by ByteDance working principles. This is not an official ByteDance project and is not affiliated with ByteDance.

Your ByteDance is a lightweight set of Codex skills for discussing, researching, planning, building, reviewing, and completing product work. It does not force every project through a fixed lifecycle. The model chooses the useful amount of process from the goal, risk, and live evidence.

## Principles

- **Outcome first:** complete the user's result, not a workflow checklist.
- **Adaptive judgment:** let the task determine research, planning, documentation, and iteration depth.
- **Minimum useful process:** act directly on simple work and add structure only when complexity justifies it.
- **Real evidence:** prefer code, tests, runtime behavior, current sources, and real feedback over status narratives.
- **Automatic learning:** turn confirmed mistakes and requirement misunderstandings into reusable prevention rules.
- **Honest delivery:** disclose verification, assumptions, failures, and remaining limits.

The project no longer requires fixed stages, three iterations, OKRs, role-play, a complete `.byte-os` document set, a harness gate, or multi-file plans.

## Install

```bash
git clone https://github.com/elan6666/your-bytedance-skills.git
cd your-bytedance-skills
cp -R byte-* ~/.codex/skills/
```

If you installed an older release, remove its deprecated skill directories separately. Copying the new release does not delete old directories.

## Quick Start

Let the system choose the right approach:

```text
$byte-do Move this product idea to the most useful next result.
```

`byte-do` is an explicit front door. It activates when you invoke `$byte-do` or
ask Byte to choose the approach, which prevents it from competing with focused
skills. Ordinary build, research, planning, or review requests can use the
matching skill directly.

Complete an outcome end to end:

```text
$byte-auto Build a working AI study assistant and verify it.
```

Or invoke a focused capability:

```text
$byte-discuss Clarify the MVP boundary for this product.
$byte-research Compare current competitors and pricing.
$byte-plan Create an appropriately detailed plan for this change.
$byte-build Implement and verify this feature.
$byte-review Review the current implementation for material issues.
$byte-status Verify the real project status.
```

## Skills

| Skill | Purpose |
|---|---|
| [`byte-do`](byte-do/SKILL.md) | Explicit adaptive entry point for mixed work |
| [`byte-auto`](byte-auto/SKILL.md) | Own an outcome through verification or a genuine blocker |
| [`byte-discuss`](byte-discuss/SKILL.md) | Discuss requirements, direction, and important tradeoffs naturally |
| [`byte-research`](byte-research/SKILL.md) | Research current evidence that can change a decision |
| [`byte-plan`](byte-plan/SKILL.md) | Plan to the depth justified by task complexity |
| [`byte-build`](byte-build/SKILL.md) | Implement focused changes with proportionate verification |
| [`byte-review`](byte-review/SKILL.md) | Find material issues in real artifacts and evidence |
| [`byte-status`](byte-status/SKILL.md) | Verify completed work, uncertainty, blockers, and next action |
| [`byte-brainstorm`](byte-brainstorm/SKILL.md) | Generate and compare substantially different directions |
| [`byte-future`](byte-future/SKILL.md) | Park an idea without expanding current scope |

## Adaptive Execution

`byte-auto` no longer runs a fixed `start → research → shape → plan → build → review → iterate → deliver` pipeline. It repeats only useful actions:

1. Inspect current files, runtime state, evidence, and prior work.
2. Choose the action with the highest value toward the goal.
3. Research, plan, implement, or review as needed.
4. Verify in proportion to risk.
5. Repair important issues and reassess completion.

A small task may finish in one pass. A difficult task may need several. Completion depends on the result and verification, not an iteration count.

## Project State

`.byte-os/` is optional. Use it when a long-running project needs resumable context. The default is one concise `.byte-os/STATE.md` containing the goal, current facts, decisions, completed work, verification, blockers, and next action.

### Automatic Lessons Notebook

When the user corrects a material misunderstanding of their request, or direct
evidence such as tests and runtime behavior confirms a reusable mistake, the
skills automatically create or update `.byte-os/LESSONS.md`. Each lesson records:

- the context;
- the mistake or misunderstanding;
- the correct understanding and evidence;
- a prevention rule for future work.

Relevant active lessons are read before new work. A recurring mistake updates the
existing entry instead of creating duplicates. Routine exploration failures,
temporary debugging noise, vague self-criticism, secrets, and sensitive user data
are not recorded.

Existing legacy Byte OS files remain useful as project evidence. Missing artifacts do not need to be recreated, and recorded stages do not force the old lifecycle.

## Migration From Removed Skills

To reduce duplication and context load, these legacy entry points were removed:

| Removed skill | Use now |
|---|---|
| `byte-start`, `byte-shape` | `byte-discuss`, `byte-plan`, `byte-do` |
| `byte-iterate`, `byte-deliver` | `byte-auto`, `byte-build` |
| `byte-next` | `byte-do`, `byte-status` |
| `byte-users` | `byte-research`, `byte-review` |
| `byte-code-rules` | Its useful principles are built into `byte-build` |
| `byte-codebase-harness` | Let `byte-plan` or `byte-build` add context only when needed |

## Attribution

Product, trademark, and company names belong to their respective owners.

中文文档：[README.md](README.md)
