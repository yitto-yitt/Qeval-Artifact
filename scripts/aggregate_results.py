from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
from pathlib import Path
from typing import Any

from common import ROOT, scrub, summary_rows, write_csv, write_jsonl


CANDIDATE_FIELDS = [
    "setting",
    "model",
    "framework",
    "class_id",
    "class_name",
    "task_id",
    "sample_index",
    "status",
    "passed",
    "case_count",
    "failed_case_count",
    "candidate_path",
    "error",
    "cases_json",
    "source_result",
]
SUMMARY_FIELDS = [
    "setting",
    "model",
    "framework",
    "class_id",
    "class_name",
    "task_count",
    "candidate_count",
    "passed_candidates",
    "candidate_pass_rate",
    "pass_at_1",
    "pass_at_5",
]


def parse_csv_list(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_class_ids(raw: str) -> list[int]:
    class_ids = [int(item) for item in parse_csv_list(raw)]
    unknown = sorted(set(class_ids) - {1, 2, 3})
    if unknown:
        raise ValueError(f"Unsupported class IDs: {unknown}")
    return sorted(set(class_ids))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass"}


def parse_int(value: Any, default: int = 0) -> int:
    text = str(value).strip()
    return int(text) if text else default


def read_candidate_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            normalized = dict(row)
            normalized["class_id"] = parse_int(normalized.get("class_id"))
            normalized["task_id"] = parse_int(normalized.get("task_id"))
            normalized["sample_index"] = parse_int(normalized.get("sample_index"), 1)
            normalized["case_count"] = parse_int(normalized.get("case_count"))
            normalized["failed_case_count"] = parse_int(normalized.get("failed_case_count"))
            normalized["passed"] = parse_bool(normalized.get("passed"))
            normalized["source_result"] = path.relative_to(ROOT).as_posix()
            rows.append(normalized)
    return rows


def candidate_files(results_root: Path, run_id: str, settings: list[str], class_ids: list[int]) -> tuple[list[Path], list[Path]]:
    found: list[Path] = []
    missing: list[Path] = []
    for setting in settings:
        for class_id in class_ids:
            path = results_root / run_id / setting / f"class{class_id}" / "candidate_results.csv"
            if path.is_file():
                found.append(path)
            else:
                missing.append(path)
    return found, missing


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    write_csv(path, summary_rows(rows), SUMMARY_FIELDS)


def write_outputs(output_dir: Path, run_id: str, input_files: list[Path], rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cleaned = [scrub(row) for row in rows]
    main_rows = [
        row
        for row in cleaned
        if not (row.get("setting") == "translation" and str(row.get("framework", "")).lower() == "qpanda2")
    ]
    qpanda2_rows = [
        row
        for row in cleaned
        if row.get("setting") == "translation" and str(row.get("framework", "")).lower() == "qpanda2"
    ]

    write_csv(output_dir / "candidate_results_all.csv", cleaned, CANDIDATE_FIELDS)
    write_jsonl(output_dir / "candidate_results_all.jsonl", cleaned)
    write_summary(output_dir / "summary_all.csv", cleaned)

    write_csv(output_dir / "candidate_results_main.csv", main_rows, CANDIDATE_FIELDS)
    write_summary(output_dir / "summary_main.csv", main_rows)

    write_csv(output_dir / "candidate_results_qpanda2.csv", qpanda2_rows, CANDIDATE_FIELDS)
    write_summary(output_dir / "summary_qpanda2.csv", qpanda2_rows)

    manifest = {
        "run_id": run_id,
        "input_files": [path.relative_to(ROOT).as_posix() for path in input_files],
        "candidate_rows_all": len(cleaned),
        "candidate_rows_main": len(main_rows),
        "candidate_rows_qpanda2": len(qpanda2_rows),
        "outputs": {
            "all_candidates": "candidate_results_all.csv",
            "all_summary": "summary_all.csv",
            "main_candidates": "candidate_results_main.csv",
            "main_summary": "summary_main.csv",
            "qpanda2_candidates": "candidate_results_qpanda2.csv",
            "qpanda2_summary": "summary_qpanda2.csv",
        },
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform()},
    }
    (output_dir / "aggregate_manifest.json").write_text(
        json.dumps(scrub(manifest), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate QEval candidate-level result bundles across classes.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--results-root", type=Path, default=ROOT / "results")
    parser.add_argument("--settings", default="direct,translation")
    parser.add_argument("--classes", default="1,2,3")
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    settings = parse_csv_list(args.settings)
    unsupported = sorted(set(settings) - {"direct", "translation"})
    if unsupported:
        raise SystemExit(f"Unsupported settings: {unsupported}")
    class_ids = parse_class_ids(args.classes)
    results_root = args.results_root.resolve()
    found, missing = candidate_files(results_root, args.run_id, settings, class_ids)
    if missing and not args.allow_missing:
        formatted = "\n".join(f"  - {path}" for path in missing)
        raise SystemExit(f"Missing expected candidate result files:\n{formatted}")
    if not found:
        raise SystemExit(f"No candidate result files found for run_id={args.run_id}")

    rows = [row for path in found for row in read_candidate_rows(path)]
    if not rows:
        raise SystemExit(f"Candidate result files contain no rows for run_id={args.run_id}")

    output_dir = results_root / args.run_id / "aggregate"
    write_outputs(output_dir, args.run_id, found, rows)
    print(f"Wrote aggregate results for {len(rows)} candidates to {output_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
