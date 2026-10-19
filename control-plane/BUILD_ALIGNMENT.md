# Build Alignment Ledger

This ledger maps prior 21amG work into the Nexus control plane without claiming unverified implementation.

## Known platform lineage

| Build | Nexus relationship | Evidence state |
|---|---|---|
| 21amG parent platform | Origin/identity plane | VERIFIED as architectural decision |
| Nexus | Brain/orchestrator/controller | VERIFIED as architectural decision |
| Runable Core v2.0 | Activation fabric: Siri/Shortcuts/webhooks | PLANNED/RECOVERED; implementation evidence must be verified |
| Agent system | Specialist autonomous workers | PLANNED/RECOVERED |
| Event bus | Cross-component coordination | PLANNED |
| Memory Broker | Typed/provenance memory | PLANNED/RECOVERED |
| Execution Router / execution_jobs | Provider execution layer | PLANNED/RECOVERED |
| 2120 AMG platform | Parent platform capabilities: dispatch, AI call center, design suite, builders | RECOVERED architecture; implementation requires repository verification |
| James Towing | Descendant application/capability | RECOVERED architecture; repository verification required |
| Repossession / Skiptrace | Descendant application/capability | RECOVERED architecture; repository verification required |
| RoastMyResume.ai | Descendant application | RECOVERED architecture; repository verification required |

## Alignment rule

Do not merge historical designs into production code merely because they appeared in prior conversations. First classify the artifact, locate repository evidence, then attach it to the Nexus registry.

## Recovery pipeline

`conversation/export -> artifact extraction -> provenance classification -> repository match -> dependency/lineage mapping -> implementation plan -> branch -> PR -> verification`

## Current GitHub visibility

The connected GitHub account currently exposes seven repositories. This repository is the control-plane anchor. The other repositories should be inventoried and mapped before code is consolidated or duplicated.

## Success condition

Nexus becomes the authoritative coordinator while individual implementations remain independently deployable. Shared identity, events, contracts, provenance and orchestration are centralized; application code stays in its appropriate descendant repository.
