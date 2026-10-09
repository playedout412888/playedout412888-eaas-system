#!/usr/bin/env python3
"""Produce a machine-readable and human-readable Daily Ops Audit report.

This is a repository/control-plane audit, not a claim that external services or
production deployments are healthy. Checks are deliberately evidence-scoped.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "daily-ops-audit"
EXPECTED_COMMANDS = {"run ai ops", "build feature", "fix", "deploy", "daily audit"}


def check(check_id: str, description: str, passed: bool, evidence: str, severity: str = "FAIL") -> dict:
    return {
        "id": check_id,
        "status": "PASS" if passed else severity,
        "description": description,
        "evidence": evidence,
    }


def main() -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    checks: list[dict] = []

    registry_path = ROOT / "control-plane" / "commands.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        commands = registry.get("commands", [])
        names = {item.get("name") for item in commands}
        sources = registry.get("sources", [])
        targets = registry.get("targets", [])
        missing = sorted(EXPECTED_COMMANDS - names)
        valid = not missing and bool(sources) and bool(targets) and all(
            isinstance(item, dict) and item.get("name") and item.get("mode")
            for item in commands
        )
        evidence = (
            f"registry_version={registry.get('version')}; command_count={len(commands)}; "
            f"missing_required={missing}; sources={sources}; targets={targets}"
        )
        checks.append(check("command-registry", "Command registry parses and contains all required commands", valid, evidence))
    except (OSError, json.JSONDecodeError, AttributeError, TypeError) as exc:
        checks.append(check("command-registry", "Command registry parses and contains all required commands", False, f"{type(exc).__name__}: {exc}"))

    library_audit = ROOT / "shortcut-library" / "tools" / "audit_library.py"
    if library_audit.is_file():
        proc = subprocess.run(
            [sys.executable, str(library_audit)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        output = (proc.stdout + proc.stderr).strip()
        checks.append(check(
            "shortcut-library",
            "Shortcut Library sanity suite passes",
            proc.returncode == 0,
            f"exit_code={proc.returncode}; output={output}",
        ))
    else:
        checks.append(check("shortcut-library", "Shortcut Library sanity suite exists", False, f"missing={library_audit.relative_to(ROOT)}"))

    workflow_path = ROOT / ".github" / "workflows" / "control-plane-audit.yml"
    try:
        workflow_text = workflow_path.read_text(encoding="utf-8")
        required_markers = {
            "manual_dispatch": "workflow_dispatch:",
            "daily_schedule": "schedule:",
            "pull_request_validation": "pull_request:",
            "report_artifact": "upload-artifact",
        }
        absent = [label for label, marker in required_markers.items() if marker not in workflow_text]
        checks.append(check(
            "audit-automation",
            "Audit workflow supports manual, scheduled, PR execution and report retention",
            not absent,
            f"workflow={workflow_path.relative_to(ROOT)}; missing_capabilities={absent}",
        ))
    except OSError as exc:
        checks.append(check("audit-automation", "Audit workflow is readable", False, f"{type(exc).__name__}: {exc}"))

    required_files = [
        "README.md",
        "control-plane/README.md",
        "control-plane/commands.json",
        "shortcut-library/README.md",
        "shortcut-library/schema/workflow-package.schema.json",
        "shortcut-library/templates/workflow-package/manifest.json",
        "shortcut-library/catalog/industries.json",
    ]
    missing_files = [item for item in required_files if not (ROOT / item).is_file()]
    checks.append(check(
        "required-assets",
        "Minimum control-plane and package-foundation files exist",
        not missing_files,
        f"required_count={len(required_files)}; missing={missing_files}",
    ))

    failures = [item for item in checks if item["status"] == "FAIL"]
    warnings = [item for item in checks if item["status"] == "WARN"]
    result = {
        "schema_version": "1.0.0",
        "audit_type": "daily-ops-control-plane",
        "generated_at": now,
        "result": "FAIL" if failures else "PASS",
        "scope": "Repository-local controls only; no external deployment, runtime, credential, or production-health claims.",
        "source": {
            "repository": os.getenv("GITHUB_REPOSITORY", "local"),
            "ref": os.getenv("GITHUB_REF", "local"),
            "sha": os.getenv("GITHUB_SHA", "unknown"),
            "run_id": os.getenv("GITHUB_RUN_ID", "local"),
            "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", "1"),
            "server_url": os.getenv("GITHUB_SERVER_URL", "https://github.com"),
        },
        "summary": {
            "checks_total": len(checks),
            "passed": sum(item["status"] == "PASS" for item in checks),
            "failed": len(failures),
            "warnings": len(warnings),
        },
        "checks": checks,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / "audit.json"
    md_path = REPORT_DIR / "audit.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Daily Ops Audit",
        "",
        f"- **Result:** {result['result']}",
        f"- **Generated (UTC):** {now}",
        f"- **Repository:** {result['source']['repository']}",
        f"- **Ref:** {result['source']['ref']}",
        f"- **Commit:** {result['source']['sha']}",
        f"- **Workflow run:** {result['source']['run_id']} (attempt {result['source']['run_attempt']})",
        f"- **Checks:** {result['summary']['passed']} passed / {result['summary']['failed']} failed / {result['summary']['warnings']} warnings",
        "",
        "> Scope is repository-local. This report does not verify external deployments, live service health, credentials, or production runtime.",
        "",
        "| Check | Status | Description | Evidence |",
        "|---|---|---|---|",
    ]
    for item in checks:
        evidence = item["evidence"].replace("|", "\\|").replace("\n", " ")
        description = item["description"].replace("|", "\\|")
        lines.append(f"| {item['id']} | **{item['status']}** | {description} | {evidence} |")
    lines.extend(["", "## Failure handling", ""])
    if failures:
        lines.extend([f"- **{item['id']}** — {item['evidence']}" for item in failures])
        lines.append("")
        lines.append("This audit exits non-zero. Fix the reported control and rerun the workflow.")
    else:
        lines.append("No repository-local blocking failures were detected by this check set.")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("\n".join(lines) + "\n")

    print(f"Daily Ops Audit: {result['result']}")
    print(f"Checks: {result['summary']['passed']} passed, {result['summary']['failed']} failed, {result['summary']['warnings']} warnings")
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {md_path.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
