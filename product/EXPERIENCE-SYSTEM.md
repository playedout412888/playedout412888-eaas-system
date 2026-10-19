# EaaS Experience System — Product Bar

Status: product requirements; implementation not yet verified.

## Product principle

EaaS is an execution product, not a chat wrapper. The interface must make powerful agent work understandable, observable, controllable, and verifiable. Visual polish is not a substitute for real execution evidence.

## Experience outcomes

1. A first-time user can start a safe, useful task without understanding agents, models, toolchains, or orchestration internals.
2. At any moment, a user can answer: what is running, why, what changed, what is blocked, what permission is needed, and what proves success.
3. Mobile users can submit work, follow progress, review diffs/evidence, and approve or reject gated actions without needing a desktop.
4. Advanced users can inspect plans, agent assignments, tool calls, artifacts, logs, retries, cost/latency, and execution provenance.
5. Every consequential state is explicit. No fake activity, fabricated metrics, or success states without evidence.

## Information architecture

- **Command Center** — task intake, live work, blockers, approvals, recent verified outcomes.
- **Missions** — task queue and execution timeline; each task has a durable ID, owner, status, scope, and cancellation/retry controls.
- **Agent Workforce** — specialist roster, capabilities, availability, assigned work, and measured quality. Do not present agents as decorative avatars.
- **Workflow / Shortcut Library** — searchable catalog, filters by industry/platform/task, compatibility, permissions, version, evidence, and install/package actions.
- **Workspaces** — repositories, connected services, environments, permissions, and toolchain capability.
- **Artifacts & Evidence** — diffs, test output, build results, reports, package manifests, checksums, and release records.
- **Approvals & Policy** — pending human gates, permission scope, impact explanation, and explicit approve/reject actions.
- **Analytics** — verified completion, failure/recovery rate, latency, cost, human intervention, and coverage by task class.
- **Settings** — identity, integrations, security, notification preferences, retention, and accessibility.

## Command Center layout

### Desktop
- Compact persistent left navigation with clear active state.
- Main work area starts with a command composer that accepts natural language and offers structured scope selectors.
- Status summary uses small, legible metrics with definitions and date ranges; never use vanity counts without meaning.
- Live mission board shows state, current stage, assigned specialists, last event, blocker/approval, and next action.
- Evidence and activity are one click away; logs do not overwhelm the primary workflow.
- Right-side contextual inspector may show selected mission details, but must collapse cleanly on smaller screens.

### Mobile
- Prioritize command intake, mission status, approvals, and evidence review.
- Use a bottom navigation or compact navigation drawer with no more than five primary destinations.
- Convert dense tables into stacked cards with the same essential fields and accessible actions.
- Preserve readable type, touch targets, sticky primary actions, and clear loading/error/offline states.
- Never require hover to discover a control or critical information.

## Visual direction

Aim for a confident, premium engineering instrument: precise typography, disciplined spacing, layered depth, restrained color, sharp data visualization, and clear status semantics. Use a dark-first canvas only if contrast and readability remain excellent; support light mode rather than hard-coding a single aesthetic. Avoid generic neon cyberpunk, gratuitous gradients, glass-on-glass cards, noisy backgrounds, excessive rounded containers, and decorative graphs with no decision value.

Visual hierarchy:
1. The user's next action.
2. Live execution state and blockers.
3. Evidence-backed outcomes.
4. Detailed telemetry and configuration.

Use motion to communicate causality and state changes: a mission moves through stages, an approval becomes actionable, or an artifact is produced. Respect reduced-motion preferences. Avoid perpetual pulsing, distracting animated backgrounds, and transitions that delay interaction.

## Interaction contract

- Every button has a real action, disabled reason, loading state, and failure feedback.
- Every long-running operation has a durable job ID, visible progress stages, cancellation semantics, and a recovery path.
- Progress must reflect observed events, not invented percentages. When percentage is unknown, show the current stage and last confirmed event.
- Destructive or externally visible operations show scope, impact, and required authorization before execution.
- A plan is distinct from execution. Preview the plan and intended write scope before a task can mutate a workspace.
- Errors explain what happened, what was preserved, and the next safe recovery action.
- Use optimistic UI only for reversible actions and reconcile with server-confirmed state.
- Keyboard navigation, focus order, visible focus, semantic labels, screen-reader announcements, and reduced motion are release requirements.

## Data visualization rules

Every chart must answer a question and identify its time window, units, source, and empty state. Prefer:
- Mission funnel: queued → planning → executing → verifying → completed/blocked.
- Reliability trend: verified completion and failure/recovery over time.
- Agent workload: active assignments and queue age.
- Workflow quality: runs, pass rate, failure categories, compatibility coverage.
- Cost/latency: median and tail values by task class, where data exists.

Never imply statistical confidence from tiny samples. Distinguish unavailable data from zero. Make chart values inspectable in an accessible table or textual summary.

## Trust and proof

- Statuses are sourced from the execution event log.
- A task is **verified** only when its configured checks produce evidence.
- Show test command, exit status, timestamp, environment, commit/ref, and artifact links when available.
- Label mock/demo data clearly and keep it out of production metrics.
- Show integration connection health and the exact permissions granted.
- Keep secrets out of client state, URLs, logs, screenshots, and exported workflow packages.

## Design and implementation gates

Before calling the console production-ready, verify:
- Responsive behavior at phone, tablet, laptop, and wide-desktop widths.
- Keyboard-only and screen-reader core flows.
- Contrast, focus, reduced-motion, and touch-target checks.
- Empty, loading, success, partial-success, blocked, timeout, retry, and offline states.
- Real backend events drive live status; refresh/reconnect does not lose mission identity.
- No fake agents, fabricated charts, dead controls, placeholder links, or unsubstantiated success badges.
- Performance budgets are measured on representative low-end mobile and desktop hardware.
- Usability tests cover first task creation, approval review, evidence inspection, and workflow discovery.

## Build sequence

1. Inventory and select the canonical application repository; confirm current frontend stack and deployment target.
2. Establish tokens, typography, layout primitives, responsive navigation, accessible components, and motion rules.
3. Build the Command Center against typed mock fixtures clearly marked as demo data.
4. Add Missions and evidence inspection using a durable job/event contract.
5. Connect real execution APIs; remove demo fixtures from production paths.
6. Add Workflow Library, approvals, analytics, and workspace administration.
7. Run visual regression, accessibility, responsive, interaction, and end-to-end checks before release.

## Current known gap

The EaaS repository's inspected root contains documentation, GitHub Actions, a command registry, and the Shortcut Library foundation, but no confirmed frontend application source or root application package manifest. The UI cannot honestly be described as implemented until a canonical app repository and actual runnable frontend are identified and verified.
