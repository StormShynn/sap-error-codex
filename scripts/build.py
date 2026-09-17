#!/usr/bin/env python3
"""Merge issues/*.json into data/issues.json and validate the schema.

Usage:  python3 scripts/build.py
"""
import json
import os
import sys
from glob import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODULES = {
    "SAP Fiori / UI5", "ABAP / Extensibility", "Transport & Release",
    "Integration / OData", "Power BI", "Microsoft Fabric", "Basis / Auth",
}
SEVERITIES = {"Blocker": 0, "High": 1, "Medium": 2, "Low": 3}
STATUSES = {"Open", "Investigating", "Resolved"}
REQUIRED = ("title", "module", "severity", "status", "symptom")


def check(issue, path, errors):
    """Append schema problems to `errors`."""
    for key in REQUIRED:
        if not issue.get(key):
            errors.append(f"{path}: missing required field '{key}'")

    if issue.get("module") and issue["module"] not in MODULES:
        errors.append(f"{path}: unknown module '{issue['module']}'")
    if issue.get("severity") and issue["severity"] not in SEVERITIES:
        errors.append(f"{path}: unknown severity '{issue['severity']}'")
    if issue.get("status") and issue["status"] not in STATUSES:
        errors.append(f"{path}: unknown status '{issue['status']}'")

    if not isinstance(issue.get("verified", False), bool):
        errors.append(f"{path}: verified must be true or false")

    solutions = issue.get("solutions") or []
    if not solutions:
        errors.append(f"{path}: needs at least one fix")
    recommended = sum(1 for s in solutions if s.get("recommended"))
    if recommended > 1:
        errors.append(f"{path}: only one fix may be recommended (found {recommended})")
    for i, solution in enumerate(solutions):
        if not solution.get("label"):
            errors.append(f"{path}: solutions[{i}] has no label")
        if not solution.get("body"):
            errors.append(f"{path}: solutions[{i}] has no body")


def main():
    paths = sorted(glob(os.path.join(ROOT, "issues", "*.json")))
    if not paths:
        print("No files found in issues/", file=sys.stderr)
        return 1

    issues, errors = [], []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as fh:
                issue = json.load(fh)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON - {exc}")
            continue

        issue["id"] = os.path.splitext(os.path.basename(path))[0]
        issue.pop("version", None)
        check(issue, rel, errors)
        issues.append(issue)

    if errors:
        print("Build stopped, fix these first:", file=sys.stderr)
        for err in errors:
            print("  -", err, file=sys.stderr)
        return 1

    issues.sort(key=lambda r: (SEVERITIES.get(r.get("severity"), 9), r["id"]))

    out_dir = os.path.join(ROOT, "data")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "issues.json"), "w", encoding="utf-8") as fh:
        json.dump(issues, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    verified = sum(1 for r in issues if r.get("verified"))
    print(f"data/issues.json: {len(issues)} entries, {verified} verified")

    by_module = {}
    for issue in issues:
        by_module[issue["module"]] = by_module.get(issue["module"], 0) + 1
    for module, count in sorted(by_module.items(), key=lambda kv: -kv[1]):
        print(f"  {count:>3}  {module}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
