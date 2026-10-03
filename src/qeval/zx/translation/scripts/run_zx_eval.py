from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = Path(__file__).resolve().parents[5]
VERIFIER_ROOT = PROJECT_ROOT / "verifiers"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "qeval_translation.json"
DEFAULT_RUN_NAME = f"{datetime.now():%Y%m%d}_crossframework_fullreduce_5sample"
EXPECTED_PYZX_VERSION = "0.10.0"


@dataclass(frozen=True)
class ClassConfig:
    source_class: str
    output_label: str
    script: Path
    std_dir: Path
    outputs_dirs: dict[str, Path]
    report_csv: str
    pattern_a: str
    pattern_b: str
    framework_a: str
    frameworks: tuple[str, ...]


@dataclass(frozen=True)
class Task:
    config: ClassConfig
    framework: str
    model: str
    code_dir: Path
    raw_out_dir: Path
    summary_out_dir: Path
    available: bool


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run full-reduce ZX verification for cross-framework 5-sample outputs and aggregate pass@k."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--run-name", default=DEFAULT_RUN_NAME)
    parser.add_argument("--class", dest="source_class")
    parser.add_argument("--classes", default=None)
    parser.add_argument("--framework", dest="framework", default=None)
    parser.add_argument("--frameworks", default=None)
    parser.add_argument("--models", default=None)
    parser.add_argument("--samples", default="1,2,3,4,5")
    parser.add_argument("--indices", default="all")
    parser.add_argument("--out-root", default=None)
    parser.add_argument("--python", type=Path, default=None)
    parser.add_argument("--summaries-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_csv_list(value: str | None, allowed: set[str] | None = None) -> list[str] | None:
    if value is None:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    if allowed is not None:
        unknown = [item for item in items if item not in allowed]
        if unknown:
            raise SystemExit(f"Unknown value(s): {', '.join(unknown)}")
    return items or None


def parse_positive_int_list(value: str | None) -> list[int]:
    if value is None:
        return [1, 2, 3, 4, 5]
    items: list[int] = []
    for part in value.split(","):
        text = part.strip()
        if not text:
            continue
        if not text.isdigit() or int(text) <= 0:
            raise SystemExit(f"Invalid positive integer: {text}")
        items.append(int(text))
    if not items:
        raise SystemExit("At least one item is required.")
    return sorted(set(items))


def parse_index_spec(value: str | None) -> list[int] | None:
    if value is None or value.strip().lower() in {"all", "*"}:
        return None
    parsed: list[int] = []
    for raw in value.split(","):
        token = raw.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start, end = int(start_text), int(end_text)
            if end < start:
                start, end = end, start
            parsed.extend(range(start, end + 1))
        else:
            parsed.append(int(token))
    return sorted(set(parsed))


def render_index_spec(indices: list[int] | None) -> str:
    if indices is None:
        return "all"
    return ",".join(str(index) for index in indices)


def normalize_framework(value: str) -> str:
    text = value.strip().lower()
    if text in {"qpanda", "qpanda3", "pyqpanda3"}:
        return "qpanda"
    return text


def framework_cli_name(value: str) -> str:
    return "Qpanda3" if normalize_framework(value) == "qpanda" else value


def resolve_project_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def resolve_output_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    return path if path.is_absolute() else (ARTIFACT_ROOT / path).resolve()


def should_skip_model_dir(name: str) -> bool:
    lowered = name.strip().lower()
    return lowered.startswith("_") or lowered in {"smoke", "__smoke__"}


def compile_idx_pattern(pattern: str) -> re.Pattern[str]:
    if "{idx}" not in pattern:
        raise ValueError("pattern must contain '{idx}'")
    rendered = re.escape(pattern).replace(r"\{idx\}", r"(?P<idx>\d+)")
    return re.compile(rf"^{rendered}$")


def compile_sample_pattern(pattern: str) -> re.Pattern[str]:
    if "{idx}" not in pattern:
        raise ValueError("pattern must contain '{idx}'")
    marker = "__IDX__"
    rendered = pattern.replace("{idx}", marker)
    escaped = re.escape(rendered).replace(re.escape(marker), r"(?P<idx>\d+)")
    if pattern.endswith(".py"):
        escaped = escaped[: -len(re.escape(".py"))] + r"(?:_s(?P<sample>\d+))?" + re.escape(".py")
    else:
        escaped += r"(?:_s(?P<sample>\d+))?"
    return re.compile(rf"^{escaped}$")


def build_sample_pattern(pattern: str, sample_index: int) -> str:
    if sample_index == 1:
        return f"{pattern[:-3]}_s1.py" if pattern.endswith(".py") else f"{pattern}_s1"
    if pattern.endswith(".py"):
        return f"{pattern[:-3]}_s{sample_index}.py"
    return f"{pattern}_s{sample_index}"


def directory_has_matching_sample_files(directory: Path, pattern: str) -> bool:
    if not directory.is_dir():
        return False
    regex = compile_sample_pattern(pattern)
    return any(child.is_file() and regex.match(child.name) for child in directory.iterdir())


def discover_models(config: ClassConfig, framework: str) -> list[str]:
    outputs_dir = config.outputs_dirs.get(framework)
    if outputs_dir is None or not outputs_dir.is_dir():
        return []
    models: list[str] = []
    for child in sorted(outputs_dir.iterdir(), key=lambda path: path.name.lower()):
        if not child.is_dir() or should_skip_model_dir(child.name):
            continue
        candidate = child / framework
        if directory_has_matching_sample_files(candidate, config.pattern_b):
            models.append(child.name)
    return models


def discover_sample_indices(directory: Path, pattern: str) -> list[int]:
    if not directory.is_dir():
        return []
    regex = compile_sample_pattern(pattern)
    found: set[int] = set()
    for child in directory.iterdir():
        if not child.is_file():
            continue
        match = regex.match(child.name)
        if match is not None:
            found.add(1 if match.group("sample") is None else int(match.group("sample")))
    return sorted(found)


def discover_task_ids(directory: Path, pattern: str, selected_indices: list[int] | None = None) -> list[int]:
    if not directory.is_dir():
        return []
    regex = compile_idx_pattern(pattern)
    found: set[int] = set()
    for child in directory.iterdir():
        if not child.is_file():
            continue
        match = regex.match(child.name)
        if match is not None:
            found.add(int(match.group("idx")))
    task_ids = sorted(found)
    if selected_indices is not None:
        wanted = set(selected_indices)
        task_ids = [task_id for task_id in task_ids if task_id in wanted]
    return task_ids


def load_class_configs(config_data: dict[str, Any]) -> dict[str, ClassConfig]:
    configs: dict[str, ClassConfig] = {}
    for source_class, item in config_data["classes"].items():
        frameworks = tuple(normalize_framework(framework) for framework in item.get("frameworks", []))
        outputs_dirs = {
            normalize_framework(framework): resolve_project_path(path)
            for framework, path in item["outputs_dirs"].items()
        }
        configs[source_class] = ClassConfig(
            source_class=source_class,
            output_label=str(item.get("output_label", source_class)),
            script=resolve_project_path(item["script"]),
            std_dir=resolve_project_path(item["std_dir"]),
            outputs_dirs=outputs_dirs,
            report_csv=str(item.get("report_csv", f"{source_class}-report.csv")),
            pattern_a=str(item.get("pattern_a", "code{idx}.py")),
            pattern_b=str(item.get("pattern_b", "code{idx}.py")),
            framework_a=normalize_framework(str(item.get("framework_a", "qiskit"))),
            frameworks=frameworks,
        )
    return configs


def build_tasks(
    classes: list[str],
    frameworks: list[str] | None,
    models: list[str] | None,
    run_root: Path,
    configs: dict[str, ClassConfig],
) -> list[Task]:
    tasks: list[Task] = []
    for source_class in classes:
        config = configs[source_class]
        selected_frameworks = frameworks if frameworks is not None else list(config.frameworks)
        for framework in selected_frameworks:
            if framework not in config.outputs_dirs:
                continue
            discovered_models = discover_models(config, framework)
            selected_models = models if models is not None else discovered_models
            outputs_dir = config.outputs_dirs[framework]
            for model in selected_models:
                code_dir = outputs_dir / model / framework
                raw_out_dir = run_root / "raw" / config.output_label / framework / model
                summary_out_dir = run_root / "summaries" / config.output_label / framework / model
                tasks.append(
                    Task(
                        config=config,
                        framework=framework,
                        model=model,
                        code_dir=code_dir,
                        raw_out_dir=raw_out_dir,
                        summary_out_dir=summary_out_dir,
                        available=model in discovered_models,
                    )
                )
    return tasks


def report_markdown_name(config: ClassConfig) -> str:
    return f"{Path(config.report_csv).stem}.md"


def sample_raw_dir(task: Task, sample_index: int) -> Path:
    return task.raw_out_dir / "samples" / f"s{sample_index}"


def sample_report_csv(task: Task, sample_index: int) -> Path:
    return sample_raw_dir(task, sample_index) / task.config.report_csv


def normalize_result(value: str | None) -> str:
    return "EQUIVALENT" if str(value or "").strip().upper() == "EQUIVALENT" else "NOT_PROVED"


def count_case_results(csv_path: Path) -> dict[str, int]:
    counts = {"total": 0, "equivalent": 0, "not_proved": 0}
    if not csv_path.exists():
        return counts
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            counts["total"] += 1
            status = normalize_result(row.get("result"))
            if status == "EQUIVALENT":
                counts["equivalent"] += 1
            else:
                counts["not_proved"] += 1
    return counts


def count_task_results(csv_path: Path) -> dict[str, int]:
    counts = {"total": 0, "equivalent": 0, "not_proved": 0}
    if not csv_path.exists():
        return counts
    grouped: dict[int, list[str]] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            index_text = str(row.get("index") or "").strip()
            if index_text.isdigit():
                grouped.setdefault(int(index_text), []).append(normalize_result(row.get("result")))
    for statuses in grouped.values():
        counts["total"] += 1
        if statuses and all(status == "EQUIVALENT" for status in statuses):
            counts["equivalent"] += 1
        else:
            counts["not_proved"] += 1
    return counts


def load_task_statuses(csv_path: Path) -> dict[int, str]:
    statuses: dict[int, list[str]] = {}
    if not csv_path.exists():
        return {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            index_text = str(row.get("index") or "").strip()
            if index_text.isdigit():
                statuses.setdefault(int(index_text), []).append(normalize_result(row.get("result")))
    return {
        task_id: "EQUIVALENT" if values and all(value == "EQUIVALENT" for value in values) else "NOT_PROVED"
        for task_id, values in statuses.items()
    }


def estimate_pass_at_k(sample_count: int, pass_count: int, k: int) -> float | None:
    if sample_count <= 0 or k <= 0 or sample_count < k:
        return None
    if pass_count <= 0:
        return 0.0
    if sample_count - pass_count < k:
        return 1.0
    return 1.0 - (math.comb(sample_count - pass_count, k) / math.comb(sample_count, k))


def format_rate(value: float | None) -> str:
    return "" if value is None else f"{value:.12g}"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def environment_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in ("pyzx", "qiskit", "qiskit-aer", "qiskit-ibm-runtime", "cirq", "pyqpanda3", "pennylane"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "NOT_INSTALLED"
    return versions


def ensure_pyzx_version() -> None:
    pyzx_version = environment_versions().get("pyzx", "NOT_INSTALLED")
    if pyzx_version != EXPECTED_PYZX_VERSION:
        raise SystemExit(f"PyZX version mismatch: expected {EXPECTED_PYZX_VERSION}, got {pyzx_version}.")


def run_sample_task(
    task: Task,
    sample_index: int,
    selected_indices: list[int] | None,
    python_executable: Path | None,
) -> int:
    out_dir = sample_raw_dir(task, sample_index)
    out_dir.mkdir(parents=True, exist_ok=True)
    mpl_config_dir = (PROJECT_ROOT / "logs" / "mplconfig").resolve()
    mpl_config_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str((python_executable or Path(sys.executable)).resolve()),
        str(task.config.script),
        "--dir-a",
        str(task.config.std_dir),
        "--dir-b",
        str(task.code_dir),
        "--pattern-a",
        task.config.pattern_a,
        "--pattern-b",
        build_sample_pattern(task.config.pattern_b, sample_index),
        "--framework-a",
        framework_cli_name(task.config.framework_a),
        "--framework-b",
        framework_cli_name(task.framework),
        "--indices",
        render_index_spec(selected_indices),
        "--out-dir",
        str(out_dir),
        "--out",
        report_markdown_name(task.config),
    ]
    print(f"\n=== {task.config.source_class} / {task.framework} / {task.model} / sample {sample_index} ===", flush=True)
    print(" ".join(f'"{part}"' if " " in part else part for part in cmd), flush=True)
    env = os.environ.copy()
    env["MPLCONFIGDIR"] = str(mpl_config_dir)
    completed = subprocess.run(cmd, cwd=str(VERIFIER_ROOT), env=env)
    return completed.returncode


def build_sample_summary_rows(
    task: Task,
    sample_indices: list[int],
) -> tuple[list[dict[str, Any]], dict[int, dict[int, str]]]:
    rows: list[dict[str, Any]] = []
    all_statuses: dict[int, dict[int, str]] = {}
    for sample_index in sample_indices:
        csv_path = sample_report_csv(task, sample_index)
        case_counts = count_case_results(csv_path)
        task_counts = count_task_results(csv_path)
        task_total = int(task_counts["total"])
        all_statuses[sample_index] = load_task_statuses(csv_path)
        rows.append(
            {
                "source_class": task.config.source_class,
                "output_label": task.config.output_label,
                "framework": task.framework,
                "model": task.model,
                "sample_index": sample_index,
                "case_total": case_counts["total"],
                "case_equivalent": case_counts["equivalent"],
                "case_not_proved": case_counts["not_proved"],
                "task_total": task_total,
                "task_equivalent": task_counts["equivalent"],
                "task_not_proved": task_counts["not_proved"],
                "task_equivalent_pct": 0.0 if task_total == 0 else task_counts["equivalent"] / task_total,
                "task_not_proved_pct": 0.0 if task_total == 0 else task_counts["not_proved"] / task_total,
                "report_dir": str(sample_raw_dir(task, sample_index)),
                "report_csv": str(csv_path),
            }
        )
    return rows, all_statuses


def build_passk_outputs(
    task: Task,
    task_ids: list[int],
    sample_indices: list[int],
    all_statuses: dict[int, dict[int, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sums = {1: 0.0, 3: 0.0, 5: 0.0}
    for task_id in task_ids:
        row: dict[str, Any] = {"task_id": task_id, "sample_count": len(sample_indices)}
        pass_count = 0
        for sample_index in sample_indices:
            status = all_statuses.get(sample_index, {}).get(task_id, "NOT_PROVED")
            row[f"sample_{sample_index}_status"] = status
            if status == "EQUIVALENT":
                pass_count += 1
        row["pass_count"] = pass_count
        for k in (1, 3, 5):
            value = estimate_pass_at_k(len(sample_indices), pass_count, k)
            row[f"pass_at_{k}"] = format_rate(value)
            sums[k] += 0.0 if value is None else value
        rows.append(row)

    task_total = len(task_ids)
    sample_count = len(sample_indices)
    summary = {
        "source_class": task.config.source_class,
        "output_label": task.config.output_label,
        "framework": task.framework,
        "model": task.model,
        "sample_count": sample_count,
        "sample_indices": sample_indices,
        "indices": task_ids,
        "task_total": task_total,
        "pass_at_1": None if task_total == 0 or sample_count < 1 else sums[1] / task_total,
        "pass_at_3": None if task_total == 0 or sample_count < 3 else sums[3] / task_total,
        "pass_at_5": None if task_total == 0 or sample_count < 5 else sums[5] / task_total,
    }
    return rows, summary


def passk_fieldnames(sample_indices: list[int]) -> list[str]:
    return ["task_id", "sample_count"] + [f"sample_{sample_index}_status" for sample_index in sample_indices] + [
        "pass_count",
        "pass_at_1",
        "pass_at_3",
        "pass_at_5",
    ]


def write_model_outputs(task: Task, sample_rows: list[dict[str, Any]], passk_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    write_csv(
        task.summary_out_dir / "sample-summary.csv",
        sample_rows,
        [
            "source_class",
            "output_label",
            "framework",
            "model",
            "sample_index",
            "case_total",
            "case_equivalent",
            "case_not_proved",
            "task_total",
            "task_equivalent",
            "task_not_proved",
            "task_equivalent_pct",
            "task_not_proved_pct",
            "report_dir",
            "report_csv",
        ],
    )
    write_csv(task.summary_out_dir / "task-passk.csv", passk_rows, passk_fieldnames(summary["sample_indices"]))
    write_json(task.summary_out_dir / "passk-summary.json", summary)


def combined_summary_row(summary: dict[str, Any], report_dir: Path) -> dict[str, Any]:
    return {
        "source_class": summary["source_class"],
        "output_label": summary["output_label"],
        "framework": summary["framework"],
        "model": summary["model"],
        "sample_count": summary["sample_count"],
        "task_total": summary["task_total"],
        "pass_at_1": format_rate(summary["pass_at_1"]),
        "pass_at_3": format_rate(summary["pass_at_3"]),
        "pass_at_5": format_rate(summary["pass_at_5"]),
        "report_dir": str(report_dir),
    }


def build_run_manifest(
    config_path: Path,
    run_root: Path,
    tasks: list[Task],
    sample_indices: list[int],
    selected_indices: list[int] | None,
) -> dict[str, Any]:
    return {
        "project_root": str(PROJECT_ROOT),
        "config_path": str(config_path),
        "run_root": str(run_root),
        "run_started_at": datetime.now().isoformat(timespec="seconds"),
        "python_executable": str(Path(sys.executable).resolve()),
        "expected_pyzx_version": EXPECTED_PYZX_VERSION,
        "environment_versions": environment_versions(),
        "sample_indices": sample_indices,
        "indices": selected_indices if selected_indices is not None else "all",
        "tasks": [
            {
                "source_class": task.config.source_class,
                "framework": task.framework,
                "model": task.model,
                "code_dir": str(task.code_dir),
                "raw_out_dir": str(task.raw_out_dir),
                "summary_out_dir": str(task.summary_out_dir),
            }
            for task in tasks
        ],
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = resolve_project_path(args.config)
    config_data = load_json(config_path)
    configs = load_class_configs(config_data)

    class_arg = args.source_class or args.classes or ",".join(configs)
    classes = parse_csv_list(class_arg, set(configs)) or []

    framework_arg = args.framework or args.frameworks
    frameworks = parse_csv_list(framework_arg)
    if frameworks is not None:
        frameworks = [normalize_framework(value) for value in frameworks]

    models = parse_csv_list(args.models)
    sample_indices = parse_positive_int_list(args.samples)
    selected_indices = parse_index_spec(args.indices)
    run_root = resolve_output_path(args.out_root) if args.out_root else (ARTIFACT_ROOT / "results" / "zx_translation" / args.run_name)
    tasks = build_tasks(classes, frameworks, models, run_root, configs)

    if args.dry_run:
        print(f"Planned tasks: {len(tasks)}")
        print(f"Indices: {render_index_spec(selected_indices)}")
        for task in tasks:
            discovered = discover_sample_indices(task.code_dir, task.config.pattern_b)
            selected = [sample for sample in sample_indices if sample in discovered]
            missing_samples = [sample for sample in sample_indices if sample not in discovered]
            if not task.available:
                status = "MISSING"
            elif missing_samples:
                status = "PARTIAL"
            else:
                status = "OK"
            print(
                f"{status:7} {task.config.source_class:5} {task.framework:10} "
                f"{task.model:35} samples={selected} {task.code_dir} -> {task.raw_out_dir}"
            )
        return 0

    ensure_pyzx_version()
    write_json(run_root / "run-manifest.json", build_run_manifest(config_path, run_root, tasks, sample_indices, selected_indices))

    combined_rows: list[dict[str, Any]] = []
    exit_code = 0
    for task in tasks:
        if not task.available:
            print(f"\n=== {task.config.source_class} / {task.framework} / {task.model} ===")
            print(f"Missing input directory or matching files: {task.code_dir}")
            exit_code = 1
            continue

        discovered_samples = discover_sample_indices(task.code_dir, task.config.pattern_b)
        selected_samples = [sample for sample in sample_indices if sample in discovered_samples]
        if len(selected_samples) != len(sample_indices):
            missing = [sample for sample in sample_indices if sample not in discovered_samples]
            print(f"\n=== {task.config.source_class} / {task.framework} / {task.model} ===")
            print(f"Missing requested samples {missing} under {task.code_dir}")
            exit_code = 1
            continue

        for sample_index in selected_samples:
            if not args.summaries_only:
                rc = run_sample_task(task, sample_index, selected_indices, args.python)
                if rc != 0:
                    exit_code = rc

        sample_rows, all_statuses = build_sample_summary_rows(task, selected_samples)
        task_ids = discover_task_ids(task.config.std_dir, task.config.pattern_a, selected_indices)
        passk_rows, summary = build_passk_outputs(task, task_ids, selected_samples, all_statuses)
        write_model_outputs(task, sample_rows, passk_rows, summary)
        combined_rows.append(combined_summary_row(summary, task.summary_out_dir))
        print(
            f"[ok] {task.config.source_class}/{task.framework}/{task.model}: "
            f"pass@1={format_rate(summary['pass_at_1'])}, "
            f"pass@3={format_rate(summary['pass_at_3'])}, "
            f"pass@5={format_rate(summary['pass_at_5'])}"
        )

    if combined_rows:
        write_csv(
            run_root / "summaries" / "passk-summary.csv",
            combined_rows,
            [
                "source_class",
                "output_label",
                "framework",
                "model",
                "sample_count",
                "task_total",
                "pass_at_1",
                "pass_at_3",
                "pass_at_5",
                "report_dir",
            ],
        )
        print(f"\nCombined pass@k summary written to {run_root / 'summaries' / 'passk-summary.csv'}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
