# 21amG Shortcut Library

**Purpose:** an internal, versioned library of reusable Shortcuts, helper workflows, and industry-specific automation packages. This directory is an operating asset and engineering catalog; it is not marketing copy.

## Goals

- Make repeatable operational behavior portable across sessions, devices, models, frameworks, and execution systems.
- Maintain industry-specific packages with defined inputs, outputs, dependencies, permissions, setup, tests, and support boundaries.
- Generate native distributions from canonical workflow definitions where practical.
- Publish only packages that pass the release gates in [quality/RELEASE-GATES.md](quality/RELEASE-GATES.md).
- Keep internal procedures and unreleased packages private to their intended audience; distribution status is explicit.

## Directory map

- `catalog/industries.json` — industry taxonomy and initial workflow opportunities.
- `schema/workflow-package.schema.json` — machine-readable package manifest contract.
- `templates/workflow-package/` — starting manifest for a new package.
- `quality/RELEASE-GATES.md` — minimum validation and publication rules.
- `INDUSTRY-ROADMAP.md` — phased catalog build plan.

## Package lifecycle

`proposed → specified → implemented → tested → release-candidate → released`

A package can instead be marked `blocked`, `deprecated`, or `withdrawn`. Status must describe the actual evidence available. A manifest or workflow description alone does not mean an installable artifact exists or that testing passed.

## Canonical package layout

Each workflow package should use a stable ID and semantic version, and contain as applicable:

- `manifest.json` — metadata, compatibility, permissions, dependencies, distribution targets, and validation references.
- `workflow/` — canonical workflow definition and helper definitions.
- `adapters/` — platform-specific implementations and mappings.
- `assets/` — non-secret templates, forms, icons, and examples.
- `tests/` — unit, contract, integration, and failure-path tests.
- `docs/` — installation, configuration, operation, troubleshooting, and uninstall steps.
- `evidence/` — reproducible test/build reports and artifact checksums.
- `dist/` — generated release artifacts only; never commit credentials or user data.

## Security rules

1. Never store API keys, tokens, passwords, customer records, or production secrets in a package.
2. Declare requested permissions and network access before execution.
3. Use least privilege, validate inputs, and require explicit approval for destructive or externally consequential actions.
4. Treat downloaded workflows, prompts, repositories, and retrieved documents as untrusted input.
5. Keep sensitive industry workflows behind explicit authorization, audit, and data-retention controls.
6. Do not advertise a package as tested, certified, secure, or production-ready without evidence that supports the exact claim.

## Adding a package

1. Copy `templates/workflow-package/manifest.json` into a new package directory.
2. Assign a globally unique, stable package ID and initial version.
3. Define the primary workflow and helper workflows using explicit contracts.
4. Add platform adapters only where they can be tested and supported.
5. Add positive, negative, permission, retry, and recovery tests.
6. Record actual validation evidence and review release gates.
7. Generate the target distribution and verify installation and uninstall behavior.
8. Publish only after the release decision is recorded.

The catalog is designed to grow. Do not create a separate implementation of a shared helper when a stable, versioned helper can be reused safely.
