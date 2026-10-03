from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

from common import (
    ROOT,
    candidate_rows_from_case_csv,
    new_run_id,
    parse_models,
    parse_task_ids,
    sanitize_text_outputs,
    task_classes,
    write_candidate_bundle,
)


DEFAULT_FRAMEWORKS = "cirq,pennylane,qpanda"
ALLOWED_FRAMEWORKS = {"cirq", "pennylane", "qpanda", "qpanda2"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate fixed cross-framework candidate programs offline.")
    parser.add_argument("--class-id", required=True, type=int, choices=(1, 2, 3))
    parser.add_argument("--models", default="all")
    parser.add_argument("--frameworks", default=DEFAULT_FRAMEWORKS)
    parser.add_argument("--tasks", default="all")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--low-shot-repeats", type=int, default=25)
    parser.add_argument("--case-timeout", type=float, default=90.0)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--execute-candidates", action="store_true")
    args = parser.parse_args()
    if not args.execute_candidates:
        parser.error("Candidate programs execute as Python code; pass --execute-candidates only in a disposable environment.")
    class_id = args.class_id
    frameworks = [item.strip().lower() for item in args.frameworks.split(",") if item.strip()]
    unknown_frameworks = sorted(set(frameworks) - ALLOWED_FRAMEWORKS)
    if unknown_frameworks:
        parser.error(f"Unsupported frameworks: {unknown_frameworks}")
    task_map = task_classes()
    class_tasks = sorted(task_id for task_id, (task_class, _) in task_map.items() if task_class == class_id)
    selected_tasks = parse_task_ids(args.tasks, class_tasks)
    if args.limit is not None:
        selected_tasks = selected_tasks[: args.limit]
    run_id = args.run_id or new_run_id()
    output_dir = ROOT / "results" / run_id / "translation" / f"class{class_id}"
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing run directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    offline_dir = ROOT / "src" / "qeval" / "offline" / "translation" / f"class{class_id}"
    sys.path.insert(0, str(offline_dir))
    base = importlib.import_module("main")
    extension = importlib.import_module("main_pennylane")
    report_dirs: list[Path] = []
    if class_id == 1:
        extension.patch_base_module()
        report_dirs = [output_dir / "native"]
        result = base.evaluate(make_namespace(args, frameworks, selected_tasks, class_id, report_dirs[0]))
        if result:
            return int(result)
    elif class_id == 2:
        base_frameworks = [framework for framework in frameworks if framework != "pennylane"]
        if base_frameworks:
            report_dir = output_dir / "native"
            report_dirs.append(report_dir)
            result = base.evaluate(make_namespace(args, base_frameworks, selected_tasks, class_id, report_dir))
            if result:
                return int(result)
        if "pennylane" in frameworks:
            report_dir = output_dir / "pennylane"
            report_dirs.append(report_dir)
            result = extension.evaluate(make_namespace(args, ["pennylane"], selected_tasks, class_id, report_dir))
            if result:
                return int(result)
    else:
        if "pennylane" in frameworks:
            extension.patch_base()
        report_dirs = [output_dir / "native"]
        result = base.evaluate(make_namespace(args, frameworks, selected_tasks, class_id, report_dirs[0]))
        if result:
            return int(result)
    sanitize_text_outputs(output_dir)
    case_results = [path / "results.csv" for path in report_dirs if (path / "results.csv").is_file()]
    if not case_results:
        raise FileNotFoundError(f"Evaluation completed without aggregate results.csv under {output_dir}")
    candidate_rows = [row for path in case_results for row in candidate_rows_from_case_csv(path, class_id)]
    if not candidate_rows:
        raise ValueError(f"No candidate-level rows parsed from {case_results}")
    write_candidate_bundle(
        output_dir,
        candidate_rows,
        {
            "run_id": run_id,
            "setting": "translation",
            "class_id": class_id,
            "task_ids": selected_tasks,
            "models": args.models,
            "frameworks": frameworks,
            "candidate_count": len(candidate_rows),
            "case_results": [path.relative_to(ROOT).as_posix() for path in case_results],
        },
    )
    print(f"Wrote {len(candidate_rows)} candidate results to {output_dir.relative_to(ROOT)}")
    return 0


def make_namespace(
    args: argparse.Namespace,
    frameworks: list[str],
    task_ids: list[int],
    class_id: int,
    reports_dir: Path,
) -> SimpleNamespace:
    base = ROOT / "src" / "qeval" / "offline" / "translation" / f"class{class_id}"
    output_dir = ROOT / "data" / "candidates" / "translation" / f"class{class_id}"
    return SimpleNamespace(
        models=args.models,
        frameworks=",".join(frameworks),
        tasks=",".join(str(task_id) for task_id in task_ids),
        limit=None,
        output_dir=str(output_dir),
        std_dir=str(base / "std"),
        reports_dir=str(reports_dir),
        repeats=args.repeats,
        low_shot_repeats=args.low_shot_repeats,
        case_timeout=args.case_timeout,
    )


if __name__ == "__main__":
    raise SystemExit(main())
