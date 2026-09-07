# Bounded goals and scheduled waiting

Use this protocol when a task includes training, a batch job, a large transfer,
or another external operation whose main next step is waiting. Keep the user's
overall outcome in persistent state across the whole cycle.

## Mutual exclusion

For the same workflow, an active goal and an enabled scheduled monitor must
never coexist. Design monitoring inside the preparation goal as a saved plan,
not a registered automation. After that goal completes, launch the long job and
activate its monitor. On completion of the job, disable and verify the monitor
before creating any next goal. Preserve unrelated jobs and automations.

## Authority and goal boundaries

Default to this cycle for complex execution tasks: substantial design and
implementation, dependent stages, or work that must survive an external wait.
Use bounded goals during actionable work and scheduled checks only when a long
external wait actually exists. A complex task without such a wait needs no
monitor. Simple edits, discussion-only, planning-only, and status-only requests
do not start this execution cycle; honor explicit user opt-outs.

This default selects the workflow; tool authority remains governed by the
current environment. Honor an explicit user request to enable this default as
standing authorization within the session, without asking again at each phase.
If higher-priority rules require an explicit goal or monitoring request that is
absent in a future session, use ordinary bounded phase state and disclose the
tool limitation instead of treating skill text as user authorization. Without a
working scheduler, disclose the missing handoff and concrete resumption action.
Never claim that future checks are active without a successful tool result.

Before creating a goal, inspect existing goals and this workflow's monitor;
confirm that its monitor is disabled or absent. Define the preparation goal
as a result achievable before the long job starts: inputs and configuration
validated, necessary code and short checks complete, launch command ready,
output locations and success/failure criteria known, and monitoring handoff
fully designed. Save the planned query command, interval, expected duration,
stall threshold, terminal evidence checks, notification triggers, stopping rules,
and next-phase criteria before closing the goal. Draft the automation prompt
here, leaving only the returned job identity to fill after launch. Do not create
or enable an automation during this goal. Include a resumable launch intent in
state before closing the goal.
Do not include training completion in this preparation goal's acceptance.
Only set a token budget when the user explicitly supplies one.

Mark the preparation goal complete only after its own acceptance is satisfied,
confirm the goal is no longer active, then launch the authorized job outside
that goal. Do not mark an existing broad
goal complete merely to stop waiting, or use blocked as a pause. Goal tools do
not imply pause, cancel, or scope-edit capabilities: if the existing goal still
requires the run result, preserve it and explain the boundary mismatch. Follow
the available tools' actual completion and blocking rules.

## Launch and handoff

Check live state before submission or retry so resumption cannot start a second
copy. After launch, persist the returned job ID (or PID plus host and start
identity), command/configuration identity, log and output paths, and submission
receipt. Launch failure is actionable repair work, not scheduled waiting.

Confirm no goal remains active before enabling the planned matching thread
heartbeat through the available automation tool, unless the user explicitly
wants a standalone task. Fill the verified job identity into the saved prompt.
Start with the interval designed during preparation; adapt it during scheduled
checks using observed progress and failure risk, respecting user constraints.
Avoid tight polling or long foreground sleep loops. Verify the saved automation and record
its ID and schedule before yielding. If registration fails, keep the live job
identity, disclose that monitoring is not active, and repair registration when
possible without relaunching the job.

Persist in the project's existing state file: overall outcome, completed phase
and evidence, pending launch or live job identity, completion criteria, monitor
ID, last checked state, and the next actionable phase. Keep one concise record.

## What each scheduled check does

Put these check and resumption rules, state location, job identity, notification
triggers, and stopping criteria in the saved automation prompt so future runs
can execute the handoff without relying on the current conversation.

First read persistent state and check for an active goal. If one already exists
for this task, disable this workflow's monitor, verify the change, and return to
the existing goal without creating another. Otherwise query the same live job:

- Running without meaningful change: stay quiet and return. Do not create a goal
  just to wait, relaunch the job, or claim progress from unchanged logs.
- Unknown, unreachable, or apparently stalled: preserve uncertainty, retry on
  schedule as appropriate, and notify when the recorded threshold or required
  user action makes it actionable. A missing PID is not terminal success.
- Terminal: verify scheduler/exit evidence and expected artifacts. Record success,
  failure, or incomplete output and a pending handoff keyed by job identity.
  Disable the matching monitor and verify it is disabled before further work.
  If disabling fails, record the error and do not create a goal; a later check
  retries monitor cleanup without re-submitting the job.

Once the monitor is confirmed disabled, check overall acceptance. If the verified
outputs already satisfy it, record completion and finish without a new goal.
Otherwise, with standing goal-mode and continuation authority, reconcile any
existing goal and create a bounded goal for substantive result validation,
analysis, repair, or the next preparation phase. Mark the handoff consumed only
after the next goal is confirmed or overall completion is recorded. Repeated or
queued checks must recognize that state and return without duplicating work.

Resume within the original scope without routine reconfirmation; do not add
experiments or unlimited retries. For a failed run, inspect evidence and define
repair acceptance before any authorized retry. If authority or inputs are
missing, report the concrete dependency instead of silently expanding the task.

Record pending handoff state before disabling the monitor so an interrupted
transition can be resumed from state and live goals. If the monitor is disabled
but goal creation fails, continue recovery in the current turn when possible;
otherwise report the exact resumption action, never claim automatic continuation
is still scheduled. Do not re-enable a monitor while a goal is active.

Repeat preparation goal (including monitor design) → complete goal → launch and
enable scheduled checks → verify termination and disable checks → next goal
only if needed. At final completion, confirm the matching monitor is disabled
and report the actual deliverable and verification limits.
