# Workflow Package Release Gates

A package is not ready to ship merely because its files exist or its happy path works. Release decisions must be evidence-based and tied to an exact version and artifact checksum.

## Gate 1 — Scope and contract

- [ ] Purpose, supported users, non-goals, and failure modes are documented.
- [ ] Input and output contracts are versioned and validated.
- [ ] Primary workflow and helper workflows have stable IDs and explicit dependencies.
- [ ] Timeouts, retries, idempotency, checkpoints, and recovery behavior are defined.
- [ ] Expected outcomes and acceptance criteria are objectively testable.

## Gate 2 — Security and privacy

- [ ] Every filesystem, network, credential, and external side effect is declared.
- [ ] Secrets are retrieved at runtime from an approved provider and never embedded in artifacts.
- [ ] Inputs are validated; prompt injection and untrusted content are treated as data, not authority.
- [ ] Least privilege and tenant boundaries are tested where applicable.
- [ ] Destructive, financial, legal, safety-sensitive, or customer-impacting actions require the appropriate authorization and review.
- [ ] Logs avoid unnecessary personal data and secret values.
- [ ] Uninstall and revocation steps are documented.

## Gate 3 — Functional verification

- [ ] Positive-path tests pass.
- [ ] Invalid input and missing-configuration tests pass.
- [ ] Permission-denied and unavailable-dependency behavior is tested.
- [ ] Retry, duplicate execution, timeout, cancellation, and recovery behavior is tested where relevant.
- [ ] Helper contracts and cross-workflow composition are tested.
- [ ] Platform-specific behavior is tested on each claimed supported target.

## Gate 4 — Installation and compatibility

- [ ] Package installs from a clean environment using the documented procedure.
- [ ] Minimum supported versions are declared and verified.
- [ ] Required accounts, entitlements, subscriptions, and platform limitations are disclosed.
- [ ] Configuration and credential setup are reproducible without embedding secrets.
- [ ] Upgrade, rollback, and uninstall procedures are tested where applicable.

## Gate 5 — Distribution integrity

- [ ] The artifact is generated from a versioned source revision.
- [ ] The manifest validates against the current schema.
- [ ] Package contents are inspected for secrets, personal data, and unexpected files.
- [ ] Artifact checksum and release evidence are recorded.
- [ ] License, redistribution rights, trademarks, and third-party licenses are reviewed.
- [ ] Release notes, support boundary, known limitations, and compatibility matrix are included.
- [ ] Catalog listing accurately reflects actual status and capabilities.

## Status semantics

- **proposed / specified:** idea or contract only; not installable.
- **implemented:** implementation exists; testing is not implied.
- **tested:** the named test suites ran; publish the results and environment.
- **release-candidate:** required release gates have evidence and are awaiting final approval.
- **released:** artifact, checksum, compatibility, license, instructions, and evidence are published.
- **blocked:** a material dependency or safety issue prevents progression.
- **deprecated / withdrawn:** use and distribution guidance is explicit.

A failed or skipped test must never be represented as a pass. A successful CI workflow does not automatically prove every supported platform or industry scenario works.
