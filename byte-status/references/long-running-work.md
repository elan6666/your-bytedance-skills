# Bounded goals and scheduled waiting

Use this protocol when a task includes training, a batch job, a large transfer,
or another external operation whose main next step is waiting. Keep the user's
overall outcome in persistent state across the whole cycle.

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

Before creating a goal, inspect any existing goal. Define the preparation goal
as a result achievable before the long job starts: inputs and configuration
validated, necessary code and short checks complete, launch command ready,
output locations and success/failure criteria known, and monitoring handoff
prepared. Include a resumable launch intent in state before closing the goal.
Do not include training completion in this preparation goal's acceptance.
Only set a token budget when the user explicitly supplies one.

Mark the preparation goal complete only after its own acceptance is satisfied,
then launch the authorized job outside that goal. Do not mark an existing broad
goal complete merely to stop waiting, or use blocked as a pause. Goal tools do
not imply pause, cancel, or scope-edit capabilities: if the existing goal still
requires the run result, preserve it and explain the boundary mismatch. Follow
the available tools' actual completion and blocking rules.

## Launch and handoff

Check live state before submission or retry so resumption cannot start a second
copy. After launch, persist the returned job ID (or PID plus host and start
identity), command/configuration identity, log and output paths, and submission
receipt. Launch failure is actionable repair work, not scheduled waiting.

Create or update a matching thread heartbeat through the available automation
tool, unless the user explicitly wants a standalone task. Choose and adapt the
check interval using expected duration, observed progress, and failure risk;
respect any user-specified interval and record a stall/review threshold. Avoid tight
polling or long foreground sleep loops. Verify the saved automation and record
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

Read persistent state and query the same live job before acting:

- Running without meaningful change: stay quiet and return. Do not create a goal
  just to wait, relaunch the job, or claim progress from unchanged logs.
- Unknown, unreachable, or apparently stalled: preserve uncertainty, retry on
  schedule as appropriate, and notify when the recorded threshold or required
  user action makes it actionable. A missing PID is not terminal success.
- Terminal: verify scheduler/exit evidence and expected artifacts. Record success,
  failure, or incomplete output; consume this terminal event once in persistent
  state so repeated checks cannot duplicate goals, retries, or downstream jobs.

After verified termination, reconcile any existing goal before creating a new
one. With standing goal-mode and continuation authority, create a bounded goal
for result validation, analysis, repair, or the next preparation phase. Resume
within the original scope without routine reconfirmation; do not add experiments
or unlimited retries. For a failed run, inspect evidence and define repair
acceptance before any authorized retry. If authority or inputs are missing,
report the concrete dependency instead of silently expanding the task.

Retire or update the old monitor once its handoff is recorded. Recover an
interrupted handoff from state and live goals before repeating mutations.
Repeat preparation goal → launch and scheduled checks → next actionable goal
until the overall acceptance is verified. At final completion, disable the
matching monitor and report the actual deliverable and verification limits.
