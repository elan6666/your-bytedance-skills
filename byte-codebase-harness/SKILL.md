---
name: byte-codebase-harness
description: Prepare a large-codebase navigation harness for Your ByteDance / Byte OS that works across Claude Code and Codex. Use when the user asks to make a repo easier for Claude/Codex to navigate, add CLAUDE.md or AGENTS.md, configure large monorepos, map a codebase, scope tests/lint by directory, reduce generated-file noise, add LSP guidance, or support subagent exploration before editing.
---

# Byte Codebase Harness

Codebase Harness makes a repository navigable before Byte OS plans or edits it. It adapts Anthropic's large-codebase guidance for Claude Code into a provider-neutral setup that also works for Codex.

## Inputs

Inspect:

```text
repo root
top-level directories
existing CLAUDE.md
existing AGENTS.md
existing .claude/settings.json
package/build/test files
.gitignore and generated/artifact directories
.byte-os/STATUS.md if present
```

## Workflow

1. Map the codebase.
   - List top-level directories and give each a one-line purpose.
   - Identify likely generated files, build outputs, vendored code, dependency directories, fixtures, and large artifacts.
   - Identify main language stacks and likely LSPs.

2. Create dual-agent context files.
   - Root `CLAUDE.md`: concise Claude Code entry context.
   - Root `AGENTS.md`: concise Codex entry context.
   - Keep root files lean: project map, critical commands, dangerous areas, conventions, and pointers.
   - Do not put specialized workflows in root context; use skills or module files instead.

3. Add module-local context where useful.
   - For the 2-3 most relevant or most active subdirectories, add local `CLAUDE.md` and `AGENTS.md`.
   - Each local file must state module purpose, build/test/lint commands, architecture constraints, and safe edit boundaries.
   - Prefer starting future agent sessions in the relevant subdirectory, while relying on parent context files for global rules.

4. Add shared Claude noise filters.
   - If Claude Code is used, create or update `.claude/settings.json`.
   - Add `permissions.deny` rules for generated files, dependency directories, build outputs, lockfile-generated artifacts, and large binary artifacts.
   - Do not deny paths that are expected to be edited, such as code generators or checked-in generated sources, unless the user confirms.

5. Record Codex-compatible guidance.
   - Codex should rely on `AGENTS.md`, `.gitignore`, `.byte-os/CODEBASE_MAP.md`, and plan-level scoped commands.
   - Do not create private Codex config unless the user explicitly asks.

6. Recommend LSP and symbol navigation.
   - Record language servers or code-intelligence plugins that would improve symbol-level navigation.
   - Prefer LSP for common symbol names, C/C++, Java, C#, PHP, TypeScript monorepos, and multi-language repositories.
   - If no LSP is available, fall back to `rg`, file reads, and local build metadata.

7. Split exploration from editing with subagents.
   - For broad unknown areas, use read-only subagents when the platform and user authorize them.
   - Assign each exploration subagent one bounded subsystem, directory, or question.
   - Require subagents to return only facts, file paths, commands discovered, risks, and suggested next context files.
   - Do not let exploration subagents edit files.
   - The main agent must decide what to change after reading the summaries.
   - If subagents are unavailable, write the same exploration summaries inline before editing.

## Artifacts

Create or update:

```text
CLAUDE.md
AGENTS.md
.claude/settings.json
.byte-os/CODEBASE_MAP.md
.byte-os/HARNESS.md
.byte-os/subagents/
.byte-os/STATUS.md
```

Optional local context files:

```text
<module>/CLAUDE.md
<module>/AGENTS.md
```

`CODEBASE_MAP.md` must include:

- Top-level directory map
- Primary stacks and package managers
- Test/lint/build command matrix by directory
- Generated/noisy paths
- LSP recommendations
- Subagent exploration candidates

When subagents are used or recommended, write:

```text
.byte-os/subagents/exploration-<area>.md
```

Each exploration file must include:

- Scope
- Files inspected
- Key facts
- Commands discovered
- Safe edit boundaries
- Risks and unknowns
- Recommended next step

`HARNESS.md` must include:

- Claude support status
- Codex support status
- Context files created
- Noise filters added
- Known gaps and follow-up setup
- Subagent exploration used or recommended
- Date reviewed

Update `STATUS.md`:

```text
Harness: ready | partial | blocked
Claude context: ready | partial | not configured
Codex context: ready | partial | not configured
Next recommended command: byte-plan
```

## Rules

- Keep root `CLAUDE.md` and `AGENTS.md` short enough to load every session.
- Move module-specific rules into subdirectory files.
- Prefer scoped tests over whole-repo tests.
- Do not rely on stale embeddings or guessed architecture.
- Use live repository inspection: `rg`, file reads, package metadata, build files, and LSP when available.
- Preserve existing human-written context files; merge instead of replacing.
- Keep subagent outputs factual and short; do not ask subagents to make product decisions.
- Revisit harness files every 3-6 months or after major model/tool changes.

## Completion Criteria

The harness is complete when Claude and Codex both have a clear entry context, noisy paths are documented or filtered, scoped verification commands are available for the active areas, and Byte OS plans can reference the right directories without rediscovering the repository from scratch.
