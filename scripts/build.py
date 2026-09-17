#!/usr/bin/env python3
"""Gộp issues/*.json thành data/issues.json và kiểm tra schema.

Chạy:  python3 scripts/build.py
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
SEVERITIES = {"Blocker": 0, "Cao": 1, "Trung bình": 2, "Thấp": 3}
STATUSES = {"Mở", "Đang điều tra", "Đã giải quyết"}
REQUIRED = ("title", "module", "severity", "status", "symptom")


def check(issue, path, errors):
    """Ghi lỗi schema vào `errors`."""
    for key in REQUIRED:
        if not issue.get(key):
            errors.append(f"{path}: thiếu trường bắt buộc '{key}'")

    if issue.get("module") and issue["module"] not in MODULES:
        errors.append(f"{path}: module không hợp lệ '{issue['module']}'")
    if issue.get("severity") and issue["severity"] not in SEVERITIES:
        errors.append(f"{path}: severity không hợp lệ '{issue['severity']}'")
    if issue.get("status") and issue["status"] not in STATUSES:
        errors.append(f"{path}: status không hợp lệ '{issue['status']}'")

    if not isinstance(issue.get("verified", False), bool):
        errors.append(f"{path}: verified phải là true/false")

    sols = issue.get("solutions") or []
    if not sols:
        errors.append(f"{path}: cần ít nhất một cách xử lý")
    recommended = sum(1 for s in sols if s.get("recommended"))
    if recommended > 1:
        errors.append(f"{path}: chỉ được một cách xử lý recommended (đang có {recommended})")
    for i, s in enumerate(sols):
        if not s.get("label"):
            errors.append(f"{path}: solutions[{i}] thiếu label")
        if not s.get("body"):
            errors.append(f"{path}: solutions[{i}] thiếu body")


def main():
    paths = sorted(glob(os.path.join(ROOT, "issues", "*.json")))
    if not paths:
        print("Không tìm thấy file nào trong issues/", file=sys.stderr)
        return 1

    issues, errors = [], []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as fh:
                issue = json.load(fh)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: JSON không hợp lệ — {exc}")
            continue

        issue["id"] = os.path.splitext(os.path.basename(path))[0]
        issue.pop("version", None)
        check(issue, rel, errors)
        issues.append(issue)

    if errors:
        print("Build dừng lại, cần sửa:", file=sys.stderr)
        for err in errors:
            print("  -", err, file=sys.stderr)
        return 1

    issues.sort(key=lambda r: (SEVERITIES.get(r.get("severity"), 9), r["id"]))

    out_dir = os.path.join(ROOT, "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "issues.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(issues, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    verified = sum(1 for r in issues if r.get("verified"))
    print(f"data/issues.json: {len(issues)} mục, {verified} đã xác minh")

    by_module = {}
    for issue in issues:
        by_module[issue["module"]] = by_module.get(issue["module"], 0) + 1
    for module, count in sorted(by_module.items(), key=lambda kv: -kv[1]):
        print(f"  {count:>3}  {module}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
