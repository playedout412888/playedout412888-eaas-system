# Voice-First AI Control Plane

This is the shared automation layer for the EaaS platform.

## Flow

`Siri Shortcut -> Command Gateway -> Orchestrator -> Specialist Agents -> GitHub/Vercel/APIs -> Verification -> Result`

## Operating principles

- Voice-first command intake from iPhone/Siri.
- Every command becomes a structured job with an ID, owner, permissions, and audit trail.
- Orchestrator decomposes work into specialist agent tasks.
- GitHub is the source of truth for code and workflow state.
- CI must pass before production deployment.
- Vercel handles application deployment where connected.
- Failed jobs retry safely; destructive operations require explicit authorization.
- Results are returned to the originating voice/chat channel.

## Command contract

```json
{
  "command": "string",
  "source": "siri|chat|webhook|schedule",
  "target": "repository-or-service",
  "mode": "plan|execute|repair|deploy|audit",
  "request_id": "uuid"
}
```

## Initial commands

- `run ai ops` — inspect health, CI, deployments, and active work.
- `build feature <description>` — create an implementation plan and execution job.
- `fix <problem>` — diagnose, patch, test, and prepare a PR.
- `deploy <service>` — verify CI and deploy through the configured deployment path.
- `daily audit` — inspect repositories, CI, deployments, and outstanding failures.

## Safety boundary

Agents may read broadly and write only within explicitly authorized repositories/services. Production-impacting changes should pass automated verification and use a review/merge gate unless the command explicitly authorizes autonomous deployment.