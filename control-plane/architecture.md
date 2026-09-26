# 21amG Nexus Control-Plane Architecture

## Purpose

This repository is the GitHub-backed control-plane implementation for the 21amG platform. **21amG is the parent/origin identity; Nexus is the brain/controller.**

Repositories are implementation artifacts. Applications and capabilities are descendants of the platform rather than isolated systems.

## Canonical operating loop

`EVENT -> OBSERVE -> UNDERSTAND -> CLASSIFY -> PLAN -> AUTHORIZE -> EXECUTE -> VALIDATE -> RECORD -> LEARN -> NEXT EVENT`

## Core planes

- **Identity:** 21amG origin, ownership, lineage.
- **Nexus:** orchestration, routing, policy, state coordination.
- **Agents:** specialist workers with bounded capabilities.
- **Skills/Capabilities:** reusable functions exposed to agents.
- **Execution:** jobs, providers, retries, verification.
- **Memory:** typed state and provenance.
- **Events:** canonical event envelopes and routing.
- **Integrations:** GitHub, Vercel, MCP, APIs and future providers.
- **Runable:** voice/Shortcuts/webhook activation fabric.
- **Applications:** descendant manifestations such as towing, repossession, skiptrace and future builds.

## Autonomy model

Runable Core v2.0 principles are represented as architectural requirements:

`orchestrator -> skills -> tools -> verifier`

Tasks use explicit contracts and definitions of done. Repair is bounded. Provider routing supports fallback. Secrets are protected. Patch/reuse is preferred over rebuild.

## Production boundary

Read-only discovery and planning are allowed by default. Writes must target an explicitly authorized repository. Production deployment, merge, destructive changes, credential changes, or external side effects require explicit authorization unless a higher-level policy explicitly grants that authority.

## Provenance

Every registry object must declare whether it is:

- VERIFIED — directly observed in a connected system.
- DERIVED — calculated from verified evidence.
- RECOVERED — supplied from historical work/conversation exports.
- PLANNED — intentionally designed but not verified as implemented.
- UNKNOWN — referenced but not yet recovered or verified.
- ILLUSTRATIVE — example only and never operational truth.

Illustrative values must never be promoted to verified metrics.
