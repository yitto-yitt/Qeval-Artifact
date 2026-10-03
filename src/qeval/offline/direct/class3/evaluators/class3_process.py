from __future__ import annotations

import copy
import importlib.metadata
import inspect
import json
import math
import platform
import re
import sys
import traceback
import types
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

from tasks import TASK_IDS, build_cases, get_task_spec


PROCESS_FIDELITY_MIN = 0.95
AVERAGE_GATE_FIDELITY_MIN = 0.95
PARAMETER_VALUES = [0.37, 0.73, 1.11, 1.57, 2.03, 2.41, 2.89, 3.17]


def thresholds() -> dict[str, float]:
    return {
        "process_fidelity_min": PROCESS_FIDELITY_MIN,
        "average_gate_fidelity_min": AVERAGE_GATE_FIDELITY_MIN,
    }


def sample_suffix(sample_index: int) -> str:
    if sample_index < 1:
        raise ValueError(f"Sample index must be positive, got {sample_index}")
    return f"_s{sample_index}"


def candidate_file_name(task_id: int, sample_index: int) -> str:
    return f"code{task_id}{sample_suffix(sample_index)}.py"


def discover_candidate_samples(dir_b: Path, task_id: int) -> list[tuple[int, Path]]:
    if dir_b.is_file():
        return [(1, dir_b)]
    if not dir_b.is_dir():
        return []
    candidates: list[tuple[int, Path]] = []
    base_path = dir_b / candidate_file_name(task_id, 1)
    if base_path.is_file():
        candidates.append((1, base_path))
    suffix_pattern = re.compile(rf"^code{task_id}_s(\d+)\.py$")
    for path in sorted(dir_b.glob(f"code{task_id}_s*.py")):
        match = suffix_pattern.match(path.name)
        if match is None:
            continue
        sample_index = int(match.group(1))
        if sample_index > 1:
            candidates.append((sample_index, path))
    return sorted(candidates, key=lambda item: item[0])


def evaluate_raw(
    dir_a: Path,
    dir_b: Path,
    task_ids: list[int] | None = None,
) -> list[dict[str, Any]]:
    selected = TASK_IDS if task_ids is None else task_ids
    all_cases = build_cases()
    results = []
    for task_id in selected:
        sample_paths = discover_candidate_samples(dir_b, task_id)
        if not sample_paths:
            sample_paths = [(1, dir_b / candidate_file_name(task_id, 1))]
        for sample_index, candidate_path in sample_paths:
            results.append(
                evaluate_task(
                    task_id,
                    all_cases[task_id],
                    dir_a,
                    dir_b,
                    sample_index,
                    candidate_path,
                )
            )
    return results


def evaluate_task(
    task_id: int,
    cases: list[dict[str, Any]],
    dir_a: Path,
    dir_b: Path,
    sample_index: int = 1,
    candidate_path: Path | None = None,
) -> dict[str, Any]:
    spec = get_task_spec(task_id)
    result: dict[str, Any] = {
        "task_id": task_id,
        "class_id": spec.class_id,
        "path_a": None,
        "path_b": None,
        "candidate_path": None,
        "sample_index": sample_index,
        "function": spec.entrypoint,
        "cases": [],
        "sample_pass": False,
        "sample_label": "raw_fail",
        "raw_status": "FAIL",
        "raw_label": "raw_fail",
        "setup_error": None,
    }

    try:
        path_a = resolve_code_path(dir_a, task_id)
        path_b = candidate_path or resolve_code_path(dir_b, task_id)
        result["path_a"] = str(path_a)
        result["path_b"] = str(path_b)
        result["candidate_path"] = str(path_b)
        func_a = load_entry_function(path_a, f"class3_a_code{task_id}", spec.entrypoint)
        func_b = load_entry_function(path_b, f"class3_b_code{task_id}_s{sample_index}", spec.entrypoint)
    except Exception as exc:
        result["setup_error"] = short_error(exc)
        return result

    all_passed = True
    for index, case in enumerate(cases, start=1):
        row = evaluate_case(func_a, func_b, case, index)
        result["cases"].append(row)
        all_passed = all_passed and row["status"] == "PASS"

    if all_passed:
        result["sample_pass"] = True
        result["sample_label"] = "RAW_PASS"
        result["raw_status"] = "PASS"
        result["raw_label"] = "RAW_PASS"
    return result


def evaluate_case(
    func_a: Callable[..., Any],
    func_b: Callable[..., Any],
    case: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    label = case.get("label", f"case_{index}")
    row = base_case_row(label)
    args = tuple(case.get("args", ()))
    kwargs = dict(case.get("kwargs", {}))

    outcome_a = call_and_capture(func_a, clone_value(args), clone_value(kwargs))
    if outcome_a["error"]:
        row["error"] = outcome_a["error"]
        return row
    outcome_b = call_and_capture(func_b, clone_value(args), clone_value(kwargs))
    if outcome_b["error"]:
        row["error"] = outcome_b["error"]
        return row

    try:
        if "compare_modified_input" in case:
            input_index = int(case["compare_modified_input"])
            reference = outcome_a["args"][input_index]
            candidate = outcome_b["args"][input_index]
            metrics = compare_outputs(reference, candidate)
        elif "compare_to_input" in case:
            input_index = int(case["compare_to_input"])
            reference = clone_value(args[input_index])
            metrics = compare_candidate_sequence_to_reference(outcome_b["value"], reference)
        else:
            metrics = compare_outputs(outcome_a["value"], outcome_b["value"])
    except Exception as exc:
        row["error"] = short_error(exc)
        return row

    row.update(metrics)
    row["status"] = "PASS" if process_metrics_pass(metrics) else "FAIL"
    return row


def base_case_row(label: Any) -> dict[str, Any]:
    return {
        "label": label,
        "status": "FAIL",
        "error": None,
        "process_fidelity": None,
        "average_gate_fidelity": None,
        "sequence_length": None,
        "item_metrics": [],
    }


def compare_outputs(reference: Any, candidate: Any) -> dict[str, Any]:
    is_sequence = isinstance(reference, (list, tuple)) or isinstance(candidate, (list, tuple))
    reference_items = normalize_output(reference)
    candidate_items = normalize_output(candidate)
    if len(reference_items) != len(candidate_items):
        raise ValueError(
            f"list length mismatch: reference={len(reference_items)}, candidate={len(candidate_items)}"
        )
    item_metrics = [
        compare_one(ref_item, cand_item)
        for ref_item, cand_item in zip(reference_items, candidate_items)
    ]
    return aggregate_item_metrics(item_metrics, is_sequence=is_sequence)


def compare_candidate_sequence_to_reference(candidate: Any, reference: Any) -> dict[str, Any]:
    candidate_items = normalize_sequence_output(candidate)
    if not candidate_items:
        raise ValueError("list length mismatch: reference>=1, candidate=0")
    item_metrics = [compare_one(reference, candidate_item) for candidate_item in candidate_items]
    return aggregate_item_metrics(item_metrics, is_sequence=True)


def normalize_output(value: Any) -> list[Any]:
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def normalize_sequence_output(value: Any) -> list[Any]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"Expected list or tuple output, got {type(value).__name__}")
    return list(value)


def compare_one(reference: Any, candidate: Any) -> dict[str, float]:
    from qiskit.quantum_info import average_gate_fidelity, process_fidelity

    reference_op = to_operator(reference)
    candidate_op = to_operator(candidate)
    return {
        "process_fidelity": float(process_fidelity(candidate_op, reference_op)),
        "average_gate_fidelity": float(average_gate_fidelity(candidate_op, reference_op)),
    }


def aggregate_item_metrics(item_metrics: list[dict[str, float]], *, is_sequence: bool) -> dict[str, Any]:
    if not item_metrics:
        raise ValueError("empty output sequence")
    min_pf = min(metric["process_fidelity"] for metric in item_metrics)
    min_agf = min(metric["average_gate_fidelity"] for metric in item_metrics)
    return {
        "process_fidelity": min_pf,
        "average_gate_fidelity": min_agf,
        "sequence_length": len(item_metrics) if is_sequence else None,
        "item_metrics": item_metrics,
    }


def process_metrics_pass(metrics: dict[str, Any]) -> bool:
    return (
        metrics["process_fidelity"] >= PROCESS_FIDELITY_MIN
        and metrics["average_gate_fidelity"] >= AVERAGE_GATE_FIDELITY_MIN
    )


def to_operator(value: Any) -> Any:
    from qiskit.circuit import Gate, Instruction, QuantumCircuit
    from qiskit.converters import dag_to_circuit
    from qiskit.dagcircuit import DAGCircuit
    from qiskit.quantum_info import Operator

    prepared = bind_parameters(value)
    if isinstance(prepared, DAGCircuit):
        prepared = dag_to_circuit(prepared)
    if isinstance(prepared, Operator):
        return prepared
    if isinstance(prepared, Gate):
        return Operator(prepared)
    if isinstance(prepared, Instruction):
        return Operator(prepared)
    if isinstance(prepared, QuantumCircuit):
        prepared = strip_measurements(prepared)
        return Operator(prepared)
    if isinstance(prepared, (int, float, complex)):
        return Operator([[prepared]])
    return Operator(prepared)


def strip_measurements(circuit: Any) -> Any:
    if not has_measurements(circuit):
        return circuit
    return circuit.remove_final_measurements(inplace=False)


def has_measurements(circuit: Any) -> bool:
    return any(instruction.operation.name == "measure" for instruction in circuit.data)


def bind_parameters(value: Any) -> Any:
    parameters = sorted(getattr(value, "parameters", []) or [], key=lambda item: item.name)
    if not parameters:
        return value
    assignments = {
        parameter: PARAMETER_VALUES[index % len(PARAMETER_VALUES)]
        for index, parameter in enumerate(parameters)
    }
    if hasattr(value, "assign_parameters"):
        return value.assign_parameters(assignments)
    if hasattr(value, "bind_parameters"):
        return value.bind_parameters(assignments)
    raise TypeError(f"Cannot bind parameters on {type(value).__name__}")


def resolve_code_path(root: Path, task_id: int) -> Path:
    root = root.expanduser().resolve()
    expected_name = f"code{task_id}.py"
    direct = root / expected_name
    if direct.is_file():
        return direct
    if root.is_file() and root.name == expected_name:
        return root
    if not root.exists():
        raise FileNotFoundError(root)

    matches = sorted(
        path
        for path in root.rglob(expected_name)
        if path.is_file() and "__pycache__" not in path.parts
    )
    if not matches:
        raise FileNotFoundError(f"{expected_name} not found under {root}")
    if len(matches) > 1:
        rendered = "\n  ".join(str(path) for path in matches)
        raise ValueError(f"multiple {expected_name} files found under {root}:\n  {rendered}")
    return matches[0]


def load_entry_function(path: Path, module_name: str, entrypoint: str) -> Callable[..., Any]:
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[module_name] = module

    source = path.read_text(encoding="utf-8-sig")
    code = compile(source, str(path), "exec")
    with prepend_sys_path(path.parent):
        exec(code, module.__dict__)

    value = vars(module).get(entrypoint)
    if value is None:
        public_functions = [
            name
            for name, candidate in vars(module).items()
            if inspect.isfunction(candidate)
            and candidate.__module__ == module.__name__
            and not name.startswith("_")
        ]
        raise ValueError(
            f"Missing required function {entrypoint!r} in {path}. "
            f"Public functions found: {public_functions}"
        )
    if not inspect.isfunction(value):
        raise TypeError(f"{entrypoint!r} in {path} is not a function")
    return value


@contextmanager
def prepend_sys_path(path: Path):
    text = str(path)
    sys.path.insert(0, text)
    try:
        yield
    finally:
        try:
            sys.path.remove(text)
        except ValueError:
            pass


def call_and_capture(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    try:
        return {"value": func(*args, **kwargs), "args": args, "kwargs": kwargs, "error": None}
    except Exception as exc:
        return {"value": None, "args": args, "kwargs": kwargs, "error": short_error(exc)}


def clone_value(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception:
        return value


def short_error(exc: BaseException) -> str:
    message = str(exc).strip()
    if not message:
        message = exc.__class__.__name__
    return message.splitlines()[0][:240]


def build_raw_details(
    sample_results: list[dict[str, Any]],
    dir_a: Path,
    dir_b: Path,
) -> dict[str, Any]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for sample in sample_results:
        grouped.setdefault(int(sample["task_id"]), []).append(sample)

    results = []
    for task_id in sorted(grouped):
        samples = sorted(grouped[task_id], key=lambda sample: int(sample.get("sample_index") or 0))
        first = samples[0]
        pass_count, pass_at_1, pass_at_3, pass_at_5 = task_pass_metrics(samples)
        best_sample = next((sample for sample in samples if sample.get("sample_pass")), None)
        results.append(
            {
                "task_id": task_id,
                "class_id": first.get("class_id"),
                "path_a": first.get("path_a"),
                "path_b": first.get("path_b"),
                "function": first.get("function"),
                "samples": samples,
                "sample_count": len(samples),
                "pass_count": pass_count,
                "pass_at_1": pass_at_1,
                "pass_at_3": pass_at_3,
                "pass_at_5": pass_at_5,
                "best_sample_index": None if best_sample is None else best_sample.get("sample_index"),
                "best_sample_path": None if best_sample is None else best_sample.get("candidate_path"),
                "raw_status": "PASS" if pass_count > 0 else "FAIL",
                "raw_label": "RAW_PASS" if pass_count > 0 else "raw_fail",
                "setup_error": None if samples else "No samples",
            }
        )

    return {
        "mode": "raw",
        "class_id": 3,
        "dir_a": str(dir_a),
        "dir_b": str(dir_b),
        "thresholds": thresholds(),
        "environment": build_environment_info(),
        "summary": build_summary_from_results(results),
        "results": results,
    }


def task_pass_metrics(samples: list[dict[str, Any]]) -> tuple[int, float | None, float | None, float | None]:
    sample_passes = [bool(sample.get("sample_pass")) for sample in samples]
    pass_count = sum(1 for passed in sample_passes if passed)
    return (
        pass_count,
        estimate_pass_at_k(len(sample_passes), pass_count, 1),
        estimate_pass_at_k(len(sample_passes), pass_count, 3),
        estimate_pass_at_k(len(sample_passes), pass_count, 5),
    )


def estimate_pass_at_k(sample_count: int, pass_count: int, k: int) -> float | None:
    if sample_count <= 0 or k <= 0 or sample_count < k:
        return None
    if pass_count <= 0:
        return 0.0
    if sample_count - pass_count < k:
        return 1.0
    return 1.0 - (math.comb(sample_count - pass_count, k) / math.comb(sample_count, k))


def build_summary_from_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    task_total = len(results)
    task_raw_pass = sum(1 for result in results if int(result.get("pass_count") or 0) > 0)
    sample_total = sum(int(result.get("sample_count") or 0) for result in results)
    sample_pass = sum(int(result.get("pass_count") or 0) for result in results)
    pass_at_1_sum = sum(float(result.get("pass_at_1") or 0.0) for result in results)
    pass_at_3_sum = sum(float(result.get("pass_at_3") or 0.0) for result in results)
    pass_at_5_sum = sum(float(result.get("pass_at_5") or 0.0) for result in results)
    return {
        "task_total": task_total,
        "task_RAW_PASS": task_raw_pass,
        "task_FAIL": task_total - task_raw_pass,
        "sample_total": sample_total,
        "sample_PASS": sample_pass,
        "sample_FAIL": sample_total - sample_pass,
        "pass_at_1_sum": pass_at_1_sum,
        "pass_at_3_sum": pass_at_3_sum,
        "pass_at_5_sum": pass_at_5_sum,
        "pass_at_1": None if task_total == 0 else pass_at_1_sum / task_total,
        "pass_at_3": None if task_total == 0 else pass_at_3_sum / task_total,
        "pass_at_5": None if task_total == 0 else pass_at_5_sum / task_total,
    }


def build_text_report(details: dict[str, Any]) -> str:
    rows = []
    for result in details.get("results", []) or []:
        code = f"code{result['task_id']}"
        rows.append(
            [
                code,
                str(result.get("sample_count") or 0),
                str(result.get("pass_count") or 0),
                format_metric(result.get("pass_at_1")),
                format_metric(result.get("pass_at_3")),
                format_metric(result.get("pass_at_5")),
                build_task_note(result),
            ]
        )

    headers = ["code", "samples", "c", "pass@1", "pass@3", "pass@5", "note"]
    t = details["thresholds"]
    summary = details["summary"]
    lines = [
        "Qiskit Class 3 raw evaluation report",
        f"dir_a: {details['dir_a']}",
        f"dir_b: {details['dir_b']}",
        (
            "process thresholds: "
            f"process_fidelity >= {t['process_fidelity_min']}, "
            f"average_gate_fidelity >= {t['average_gate_fidelity_min']}"
        ),
        "",
        format_table(headers, rows),
    ]
    lines.extend(
        [
            "",
            "overall summary:",
            f"task_RAW_PASS: {summary.get('task_RAW_PASS', 0)} / {summary.get('task_total', 0)}",
            f"task_FAIL: {summary.get('task_FAIL', 0)} / {summary.get('task_total', 0)}",
            f"sample_PASS: {summary.get('sample_PASS', 0)} / {summary.get('sample_total', 0)}",
            f"sample_FAIL: {summary.get('sample_FAIL', 0)} / {summary.get('sample_total', 0)}",
            f"pass@1: {format_rate(summary.get('pass_at_1'))}",
            f"pass@3: {format_rate(summary.get('pass_at_3'))}",
            f"pass@5: {format_rate(summary.get('pass_at_5'))}",
        ]
    )
    return "\n".join(lines) + "\n"


def build_task_note(result: dict[str, Any]) -> str:
    if result.get("setup_error"):
        return first_line(result.get("setup_error"))
    if int(result.get("pass_count") or 0) > 0:
        return ""
    for sample in result.get("samples", []) or []:
        if sample.get("setup_error"):
            return first_line(sample.get("setup_error"))
        for case in sample.get("cases", []) or []:
            if case.get("error"):
                return first_line(case.get("error"))
    if not result.get("samples"):
        return "No samples"
    return "All samples failed"


def format_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    lines = [
        " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)),
        "-+-".join("-" * width for width in widths),
    ]
    for row in rows:
        lines.append(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))
    return "\n".join(lines)


def format_case_row(code: str, row: dict[str, Any], raw_label: str) -> dict[str, str]:
    if row.get("sequence_length"):
        value = (
            f"n={row.get('sequence_length')}, "
            f"min_pf={format_metric(row.get('process_fidelity'))}, "
            f"min_agf={format_metric(row.get('average_gate_fidelity'))}"
        )
    else:
        value = (
            f"pf={format_metric(row.get('process_fidelity'))}, "
            f"agf={format_metric(row.get('average_gate_fidelity'))}"
        )
    return {
        "code": code,
        "case": str(row["label"]),
        "metric": "process",
        "value": value,
        "status": row["status"],
        "label": raw_label,
        "note": row.get("error") or "",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build_environment_info() -> dict[str, Any]:
    info: dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {},
        "qiskit_symbols": {},
    }
    for package in ("qiskit", "qiskit-aer", "qiskit-ibm-runtime"):
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = None
        info["packages"][package] = version

    try:
        import qiskit.quantum_info as quantum_info

        for name in (
            "Operator",
            "process_fidelity",
            "average_gate_fidelity",
            "random_unitary",
        ):
            info["qiskit_symbols"][f"qiskit.quantum_info.{name}"] = hasattr(quantum_info, name)
    except Exception as exc:
        info["qiskit_quantum_info_import_error"] = repr(exc)

    return info


def build_environment_report(info: dict[str, Any] | None = None) -> str:
    env = info or build_environment_info()
    lines = [
        "Qiskit Class 3 raw evaluation environment",
        f"python: {env.get('python')}",
        f"platform: {env.get('platform')}",
    ]
    for package, version in env.get("packages", {}).items():
        lines.append(f"{package}: {version or 'not installed'}")
    for symbol, exists in env.get("qiskit_symbols", {}).items():
        lines.append(f"{symbol} exists: {exists}")
    if "qiskit_quantum_info_import_error" in env:
        lines.append(f"qiskit.quantum_info import error: {env['qiskit_quantum_info_import_error']}")
    return "\n".join(lines) + "\n"


def max_width(rows: list[dict[str, str]], key: str, header: str) -> int:
    return max([len(header), *(len(str(row[key])) for row in rows)])


def format_metric(value: Any) -> str:
    if value in ("", None):
        return ""
    number = float(value)
    if math.isnan(number):
        return "nan"
    return f"{number:.12g}"


def format_rate(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"{float(value):.2f}"


def first_line(value: str | None) -> str:
    if not value:
        return ""
    return str(value).strip().splitlines()[0]
