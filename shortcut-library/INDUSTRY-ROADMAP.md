# Industry Library Roadmap

This is an internal build sequence. Priorities are hypotheses to validate, not claims of completed catalog coverage.

## Wave 0 — Shared foundation

Build the package schema, catalog, reusable helper contracts, artifact builder, validation harness, release evidence format, and internal package index.

Shared helper candidates:

- Normalize and validate inputs.
- Resolve secrets through runtime references.
- Check authorization and request approvals.
- Emit redacted audit events.
- Retry transient failures safely.
- Save and restore checkpoints.
- Normalize tool and model responses.
- Capture test/build evidence.
- Generate installation and uninstall instructions.
- Build, checksum, and inspect distribution artifacts.

## Wave 1 — Internal dogfood and immediate operational value

1. Software engineering and repository operations.
2. Small-business operations.
3. Automotive, towing, and vehicle recovery.

Use these packages to exercise repository changes, client delivery, field-service paperwork, dispatch handoffs, and repeatable operational tasks. Automotive recovery workflows must include explicit jurisdictional and authorization boundaries.

## Wave 2 — Common service businesses

- Home services and field service.
- Logistics and fleet operations.
- Professional services and consulting.
- Marketing and creative agencies.
- Real estate and property management.
- Retail and e-commerce.

## Wave 3 — Higher-governance domains

- Construction and skilled trades.
- Education and training.
- Healthcare administration.
- Legal administration.
- Finance and bookkeeping administration.
- IT operations and cybersecurity.
- Hospitality, events, nonprofit operations, and creator/media workflows.

These domains require additional review for privacy, regulated information, safety, licensing, professional oversight, and consequential decisions. Inclusion in the catalog does not imply legal or regulatory compliance.

## Definition of a complete industry pack

Each industry pack should include:

1. Industry overview and scope boundaries.
2. Use-case catalog ranked by value, risk, and implementation cost.
3. Primary workflows plus shared helper workflows.
4. Platform and integration compatibility matrix.
5. Configuration templates and sample data without real personal information.
6. Unit, contract, integration, negative-path, and recovery tests.
7. Security/privacy review appropriate to the domain.
8. Install, configure, operate, troubleshoot, upgrade, and uninstall documentation.
9. Package manifest, release notes, artifact checksum, and validation evidence.
10. Catalog metadata, edition/license eligibility, and support boundary.

## Prioritization score

Score candidate workflows from 1–5 for repeat demand, customer value, cross-platform reuse, testability, and implementation effort. Increase priority for high repeat demand, value, reuse, and testability; reduce it for high effort and high risk. Do not ship a high-risk workflow solely because it scores well commercially.

## Release principle

Prefer a smaller number of deeply tested, useful packages over a large catalog of shallow templates. Catalog breadth can grow in parallel with automated testing, but released status is earned package by package.
