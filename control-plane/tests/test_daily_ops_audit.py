"""Regression tests for Daily Ops Audit portfolio configuration handling."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "daily_ops_audit.py"
SPEC = importlib.util.spec_from_file_location("daily_ops_audit", MODULE_PATH)
daily_ops_audit = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(daily_ops_audit)


class EmptyPortfolioConfigurationTests(unittest.TestCase):
    def _run_audit(self, target_content: str | None, *, create_target_file: bool = True) -> dict:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "control-plane").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "control-plane" / "commands.json").write_text(
                json.dumps({"commands": [], "sources": [], "targets": []}), encoding="utf-8"
            )
            (root / ".github" / "workflows" / "control-plane-audit.yml").write_text(
                "workflow_dispatch:\nschedule:\npull_request:\nupload-artifact\nAUDIT_GITHUB_TOKEN:\n",
                encoding="utf-8",
            )
            for relative in (
                "README.md",
                "control-plane/README.md",
                "control-plane/commands.json",
                "shortcut-library/README.md",
                "shortcut-library/schema/workflow-package.schema.json",
                "shortcut-library/templates/workflow-package/manifest.json",
                "shortcut-library/catalog/industries.json",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)

            targets_path = root / "control-plane" / "audit-targets.json"
            if create_target_file:
                targets_path.write_text(target_content or "", encoding="utf-8")
            report_dir = root / "reports" / "daily-ops-audit"
            with (
                patch.object(daily_ops_audit, "ROOT", root),
                patch.object(daily_ops_audit, "TARGETS_PATH", targets_path),
                patch.object(daily_ops_audit, "REPORT_DIR", report_dir),
            ):
                exit_code = daily_ops_audit.main()
            self.assertNotEqual(exit_code, 0, "invalid or empty portfolio configuration must not pass")
            report = json.loads((report_dir / "audit.json").read_text(encoding="utf-8"))
            return report

    def test_empty_repository_list_generates_report(self) -> None:
        report = self._run_audit(json.dumps({"repositories": []}))
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(any(c["id"] == "portfolio-config" and c["status"] == "FAIL" for c in report["checks"]))

    def test_malformed_json_generates_report(self) -> None:
        report = self._run_audit("{not-json")
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(any(c["id"] == "portfolio-config" and c["status"] == "FAIL" for c in report["checks"]))

    def test_missing_file_generates_report(self) -> None:
        report = self._run_audit(None, create_target_file=False)
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(any(c["id"] == "portfolio-config" and c["status"] == "FAIL" for c in report["checks"]))


if __name__ == "__main__":
    unittest.main()
