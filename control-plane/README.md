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
## Daily Ops Audit

The `control-plane/daily_ops_audit.py` runner executes on pull requests, pushes to supported branches, manual dispatch, and the daily UTC schedule. It emits a Markdown summary and JSON evidence report, uploads both as a 30-day Actions artifact, and checks the configured repository portfolio read-only.

### Private-repository coverage

The built-in `GITHUB_TOKEN` is scoped to this repository. To read private repositories listed in `control-plane/audit-targets.json`, configure an Actions repository secret named `AUDIT_GITHUB_TOKEN`. Use a fine-grained token restricted to the intended repositories with read-only **Metadata, Actions, and Pull requests** permissions. The workflow does not use this token for writes. Without it, inaccessible private targets are marked **WARN** and the overall audit is **DEGRADED**, rather than falsely reporting full coverage.

Never put a token in source files, workflow YAML literals, issues, or logs. Rotate or revoke it if exposed. Public targets are retried without the repository-scoped token when an authenticated request returns 404.
