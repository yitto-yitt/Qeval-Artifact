from __future__ import annotations

import csv
import json
import math
import platform
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]


def task_classes() -> dict[int, tuple[int, str]]:
    with (ROOT / "data" / "retained_tasks.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            int(row["task_id"]): (int(row["class_id"]), row["class_name"])
            for row in csv.DictReader(handle)
        }


def parse_models(raw: str, data_root: Path) -> list[str]:
    if raw.strip().lower() == "all":
        return sorted(path.name for path in data_root.iterdir() if path.is_dir() and not path.name.startswith("_"))
    return sorted({item.strip() for item in raw.split(",") if item.strip()})


def parse_task_ids(raw: str, available: Iterable[int]) -> list[int]:
    allowed = set(available)
    if raw.strip().lower() == "all":
        return sorted(allowed)
    selected = sorted({int(item.strip()) for item in raw.split(",") if item.strip()})
    unknown = sorted(set(selected) - allowed)
    if unknown:
        raise ValueError(f"Task IDs are not in the selected class: {unknown}")
    return selected


def new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): scrub(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub(item) for item in value]
    if isinstance(value, tuple):
        return [scrub(item) for item in value]
    if isinstance(value, str):
        text = value
        for path in (str(ROOT), str(ROOT).replace("\\", "/")):
            text = text.replace(path, ".")
        workspace = str(ROOT.parent)
        for path in (workspace, workspace.replace("\\", "/")):
            text = text.replace(path, "<WORKSPACE>")
        return text
    return value


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(scrub(row), ensure_ascii=False, sort_keys=True) + "\n")


def candidate_rows_from_case_csv(path: Path, class_id: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, int, int], list[dict[str, str]]] = defaultdict(list)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row.get("task_id") or not row.get("sample_index"):
                continue
            key = (row.get("model", ""), row.get("framework", ""), int(row["task_id"]), int(row["sample_index"]))
            grouped[key].append(row)
    rows: list[dict[str, Any]] = []
    classes = task_classes()
    for (model, framework, task_id, sample_index), cases in sorted(grouped.items()):
        statuses = [str(case.get("status", "")).upper() for case in cases]
        if statuses and all(status in {"PASS", "RAW_PASS"} for status in statuses):
            status = "PASS"
        elif any(status in {"ERROR", "SETUP_ERROR"} for status in statuses):
            status = "ERROR"
        else:
            status = "FAIL"
        error_values = sorted({case.get("error", "").strip() for case in cases if case.get("error", "").strip()})
        rows.append(
            {
                "setting": "translation",
                "model": model,
                "framework": framework,
                "class_id": class_id,
                "class_name": classes.get(task_id, (class_id, ""))[1],
                "task_id": task_id,
                "sample_index": sample_index,
                "status": status,
                "passed": status == "PASS",
                "case_count": len(cases),
                "failed_case_count": sum(case_status not in {"PASS", "RAW_PASS"} for case_status in statuses),
                "error": "; ".join(error_values),
            }
        )
    return rows


def summary_rows(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in candidate_rows:
        buckets[(row["setting"], row["model"], row["framework"], int(row["class_id"]))].append(row)
    summaries: list[dict[str, Any]] = []
    for (setting, model, framework, class_id), rows in sorted(buckets.items()):
        tasks: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            tasks[int(row["task_id"])].append(row)
        pass_at_one: list[float] = []
        pass_at_five: list[float] = []
        for task_rows in tasks.values():
            sample_count = len(task_rows)
            pass_count = sum(bool(row["passed"]) for row in task_rows)
            if sample_count:
                pass_at_one.append(pass_count / sample_count)
            if sample_count >= 5:
                pass_at_five.append(1.0 if pass_count else 0.0)
        passed = sum(bool(row["passed"]) for row in rows)
        summaries.append(
            {
                "setting": setting,
                "model": model,
                "framework": framework,
                "class_id": class_id,
                "class_name": task_classes().get(next(iter(tasks)), (class_id, ""))[1] if tasks else "",
                "task_count": len(tasks),
                "candidate_count": len(rows),
                "passed_candidates": passed,
                "candidate_pass_rate": passed / len(rows) if rows else None,
                "pass_at_1": sum(pass_at_one) / len(pass_at_one) if pass_at_one else None,
                "pass_at_5": sum(pass_at_five) / len(pass_at_five) if pass_at_five else None,
            }
        )
    return summaries


def write_candidate_bundle(output_dir: Path, rows: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    fields = [
        "setting", "model", "framework", "class_id", "class_name", "task_id", "sample_index",
        "status", "passed", "case_count", "failed_case_count", "candidate_path", "error", "cases_json",
    ]
    cleaned = [scrub(row) for row in rows]
    write_csv(output_dir / "candidate_results.csv", cleaned, fields)
    write_jsonl(output_dir / "candidate_results.jsonl", cleaned)
    summaries = summary_rows(cleaned)
    summary_fields = [
        "setting", "model", "framework", "class_id", "class_name", "task_count", "candidate_count",
        "passed_candidates", "candidate_pass_rate", "pass_at_1", "pass_at_5",
    ]
    write_csv(output_dir / "summary.csv", summaries, summary_fields)
    payload = {
        "run": manifest,
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform()},
        "candidate_rows": len(cleaned),
        "summary_rows": len(summaries),
    }
    (output_dir / "run_manifest.json").write_text(
        json.dumps(scrub(payload), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def sanitize_text_outputs(directory: Path) -> None:
    for path in directory.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".csv", ".json", ".jsonl", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        sanitized = scrub(text)
        if sanitized != text:
            path.write_text(sanitized, encoding="utf-8", newline="\n")

