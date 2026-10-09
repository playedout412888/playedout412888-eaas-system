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
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "daily-ops-audit"
TARGETS_PATH = ROOT / "control-plane" / "audit-targets.json"
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

    # Portfolio checks are read-only. Inaccessible/private repositories are WARN,
    # not silently treated as healthy. Only recent, latest-per-workflow failures
    # are blocking; a repo with no Actions history is explicitly reported.
    portfolio_summary = {"configured": 0, "reachable": 0, "workflow_failures": 0, "without_workflow_history": 0}
    try:
        target_config = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
        targets = target_config.get("repositories", [])
        portfolio_summary["configured"] = len(targets)
    except (OSError, json.JSONDecodeError, AttributeError, TypeError) as exc:
        targets = []
        checks.append(check("portfolio-config", "Repository portfolio configuration is valid", False, f"{type(exc).__name__}: {exc}"))

    dedicated_audit_token = os.getenv("AUDIT_GITHUB_TOKEN", "")
    token = dedicated_audit_token or os.getenv("GITHUB_TOKEN", "")
    api_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "21amG-Daily-Ops-Audit",
    }
    if token:
        api_headers["Authorization"] = f"Bearer {token}"

    def github_get(api_path: str):
        request = Request("https://api.github.com" + api_path, headers=api_headers)
        try:
            with urlopen(request, timeout=12) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            # The workflow's built-in GITHUB_TOKEN is repository-scoped. Retry
            # a 404 anonymously so public cross-repository targets remain auditable.
            # A private target still returns 404 and is reported as inaccessible.
            if exc.code != 404 or not token:
                raise
            public_headers = {key: value for key, value in api_headers.items() if key != "Authorization"}
            public_request = Request("https://api.github.com" + api_path, headers=public_headers)
            with urlopen(public_request, timeout=12) as response:
                return json.loads(response.read().decode("utf-8"))

    if targets:
        for target in targets:
            full_name = target.get("full_name", "")
            if "/" not in full_name:
                checks.append(check("portfolio-target", "Portfolio target has owner/repository format", False, f"invalid_target={full_name}"))
                continue
            try:
                repo_info = github_get(f"/repos/{full_name}")
                portfolio_summary["reachable"] += 1
                pulls = github_get(f"/repos/{full_name}/pulls?state=open&per_page=100")
                default_branch = repo_info.get("default_branch", "unknown")
                checks.append(check(
                    f"repo:{full_name}:reachable",
                    f"Repository is readable and default branch is known ({target.get('role', 'unspecified')})",
                    bool(default_branch),
                    f"default_branch={default_branch}; visibility={repo_info.get('visibility', 'unknown')}; open_prs={len(pulls) if isinstance(pulls, list) else 'unknown'}",
                ))
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
                code = getattr(exc, "code", None)
                checks.append(check(
                    f"repo:{full_name}:reachable",
                    f"Repository is readable ({target.get('role', 'unspecified')})",
                    False,
                    f"api_error={code or type(exc).__name__}; details={str(exc)[:240]}; "
                    + ("Set the AUDIT_GITHUB_TOKEN Actions secret with read-only access to this private repository." if code == 404 and not dedicated_audit_token else "Check token permissions, rate limit, network, or repository visibility."),
                    severity="WARN",
                ))
                continue

            try:
                payload = github_get(f"/repos/{full_name}/actions/runs?per_page=30")
                runs = payload.get("workflow_runs", []) if isinstance(payload, dict) else []
                latest_by_workflow = {}
                for run in runs:
                    workflow_id = run.get("workflow_id", run.get("name", "unknown"))
                    if workflow_id not in latest_by_workflow:
                        latest_by_workflow[workflow_id] = run
                if not latest_by_workflow:
                    portfolio_summary["without_workflow_history"] += 1
                    checks.append(check(
                        f"repo:{full_name}:actions",
                        "Recent GitHub Actions health is observable",
                        False,
                        "No workflow runs returned; CI health is unknown, not assumed healthy",
                        severity="WARN",
                    ))
                    continue

                now_utc = datetime.now(timezone.utc)
                recent_failures = []
                recent_unknown = []
                for run in latest_by_workflow.values():
                    created = run.get("created_at")
                    try:
                        age_days = (now_utc - datetime.fromisoformat(created.replace("Z", "+00:00"))).total_seconds() / 86400
                    except (AttributeError, ValueError):
                        age_days = 9999
                    conclusion = run.get("conclusion")
                    if age_days <= 7 and conclusion in {"failure", "timed_out", "action_required"}:
                        recent_failures.append({
                            "workflow": run.get("name"),
                            "conclusion": conclusion,
                            "created_at": created,
                            "url": run.get("html_url"),
                        })
                    elif age_days <= 7 and run.get("status") == "completed" and conclusion not in {"success", "skipped", "neutral", "cancelled"}:
                        recent_unknown.append({"workflow": run.get("name"), "conclusion": conclusion, "created_at": created})
                if recent_failures:
                    portfolio_summary["workflow_failures"] += len(recent_failures)
                evidence = (
                    f"latest_workflows_checked={len(latest_by_workflow)}; "
                    f"recent_failures={json.dumps(recent_failures, separators=(',', ':'))}; "
                    f"recent_unknown={json.dumps(recent_unknown, separators=(',', ':'))}"
                )
                checks.append(check(
                    f"repo:{full_name}:actions",
                    "Latest-per-workflow GitHub Actions results are healthy over the last 7 days",
                    not recent_failures and not recent_unknown,
                    evidence,
                    severity="FAIL" if recent_failures else "WARN",
                ))
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
                code = getattr(exc, "code", None)
                checks.append(check(
                    f"repo:{full_name}:actions",
                    "GitHub Actions health is readable",
                    False,
                    f"api_error={code or type(exc).__name__}; details={str(exc)[:240]}",
                    severity="WARN",
                ))

        failures = [item for item in checks if item["status"] == "FAIL"]
    warnings = [item for item in checks if item["status"] == "WARN"]
    result = {
        "schema_version": "1.0.0",
        "audit_type": "daily-ops-control-plane",
        "generated_at": now,
        "result": "FAIL" if failures else ("DEGRADED" if warnings else "PASS"),
        "scope": "Repository-local controls only; no external deployment, runtime, credential, or production-health claims.",
        "source": {
            "repository": os.getenv("GITHUB_REPOSITORY", "local"),
            "ref": os.getenv("GITHUB_REF", "local"),
            "sha": os.getenv("GITHUB_SHA", "unknown"),
            "run_id": os.getenv("GITHUB_RUN_ID", "local"),
            "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT", "1"),
            "server_url": os.getenv("GITHUB_SERVER_URL", "https://github.com"),
        },
        "portfolio": portfolio_summary,
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
        f"- **Portfolio:** {portfolio_summary['reachable']}/{portfolio_summary['configured']} repositories readable; {portfolio_summary['workflow_failures']} recent workflow failures; {portfolio_summary['without_workflow_history']} repositories without workflow history",
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
    print(f"Portfolio: {portfolio_summary['reachable']}/{portfolio_summary['configured']} repositories readable; {portfolio_summary['workflow_failures']} recent workflow failures; {portfolio_summary['without_workflow_history']} without workflow history")
    for item in checks:
        print(f"[{item['status']}] {item['id']}: {item['evidence']}")
    print(f"JSON report: {json_path.relative_to(ROOT)}")
    print(f"Markdown report: {md_path.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
