from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

from common import ROOT, new_run_id, parse_models, parse_task_ids, task_classes, write_candidate_bundle


EVALUATORS = {
    1: "evaluators.class1_distribution",
    2: "evaluators.class2_state",
    3: "evaluators.class3_process",
}
EVALUATOR_NAMES = {1: "class1_distribution", 2: "class2_state", 3: "class3_process"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the fixed direct-Qiskit candidate programs.")
    parser.add_argument("--class-id", required=True, type=int, choices=(1, 2, 3))
    parser.add_argument("--models", default="all")
    parser.add_argument("--tasks", default="all")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--execute-candidates", action="store_true")
    args = parser.parse_args()
    if not args.execute_candidates:
        parser.error("Candidate programs execute as Python code; pass --execute-candidates only in a disposable environment.")
    class_id = args.class_id
    tasks = task_classes()
    class_tasks = sorted(task_id for task_id, (task_class, _) in tasks.items() if task_class == class_id)
    selected_tasks = parse_task_ids(args.tasks, class_tasks)
    if args.limit is not None:
        selected_tasks = selected_tasks[: args.limit]
    class_dir = ROOT / "src" / "qeval" / "offline" / "direct" / f"class{class_id}"
    sys.path.insert(0, str(class_dir))
    evaluator_module = importlib.import_module(EVALUATORS[class_id])
    evaluator = evaluator_module.evaluate_raw
    models_root = ROOT / "data" / "candidates" / "direct" / f"class{class_id}"
    models = parse_models(args.models, models_root)
    run_id = args.run_id or new_run_id()
    output_dir = ROOT / "results" / run_id / "direct" / f"class{class_id}"
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing run directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    reference_dir = class_dir / "std"
    for model in models:
        candidate_dir = models_root / model / "qiskit"
        if not candidate_dir.is_dir():
            raise FileNotFoundError(f"Candidate directory not found: {candidate_dir}")
        results = evaluator(reference_dir, candidate_dir, selected_tasks)
        for result in results:
            task_id = int(result["task_id"])
            status = str(result.get("raw_status", result.get("sample_status", "ERROR"))).upper()
            cases = result.get("cases", [])
            rows.append(
                {
                    "setting": "direct",
                    "model": model,
                    "framework": "qiskit",
                    "class_id": class_id,
                    "class_name": tasks[task_id][1],
                    "task_id": task_id,
                    "sample_index": int(result.get("sample_index", 1)),
                    "status": "PASS" if status in {"PASS", "RAW_PASS"} else "FAIL",
                    "passed": status in {"PASS", "RAW_PASS"},
                    "case_count": len(cases),
                    "failed_case_count": sum(str(case.get("status", "")).upper() != "PASS" for case in cases),
                    "candidate_path": result.get("candidate_path"),
                    "error": result.get("setup_error") or "",
                    "cases_json": json.dumps(cases, ensure_ascii=False, sort_keys=True),
                }
            )
    write_candidate_bundle(
        output_dir,
        rows,
        {
            "run_id": run_id,
            "setting": "direct",
            "class_id": class_id,
            "task_ids": selected_tasks,
            "models": models,
            "candidate_count": len(rows),
        },
    )
    print(f"Wrote {len(rows)} candidate results to {output_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
