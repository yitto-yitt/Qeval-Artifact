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

import numpy as np

from tasks import TASK_IDS, build_cases, get_task_spec


STATE_FIDELITY_MIN = 0.95
TRACE_DISTANCE_MAX = 0.10
PURITY_DIFF_MAX = 0.05
REFERENCE_STATE_TASK_IDS = {2, 3, 5, 6, 11, 39, 62, 66, 139}
CIRCUIT_STATE_TASK_IDS = {3, 5, 6, 62, 66}
MEASURED_CIRCUIT_TASK_IDS = {3, 66}


def thresholds() -> dict[str, float]:
    return {
        "state_fidelity_min": STATE_FIDELITY_MIN,
        "trace_distance_max": TRACE_DISTANCE_MAX,
        "purity_diff_max": PURITY_DIFF_MAX,
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
        func_b = load_entry_function(path_b, f"class2_b_code{task_id}_s{sample_index}", spec.entrypoint)
        func_a = None
        if task_id in REFERENCE_STATE_TASK_IDS:
            func_a = load_entry_function(path_a, f"class2_a_code{task_id}", spec.entrypoint)
    except Exception:
        result["setup_error"] = traceback.format_exc().strip()
        return result

    all_passed = True
    for index, case in enumerate(cases, start=1):
        row = evaluate_case(task_id, func_b, case, index, func_a)
        result["cases"].append(row)
        all_passed = all_passed and row["status"] == "PASS"

    if all_passed:
        result["sample_pass"] = True
        result["sample_label"] = "RAW_PASS"
        result["raw_status"] = "PASS"
        result["raw_label"] = "RAW_PASS"
    return result


def evaluate_case(
    task_id: int,
    func_b: Callable[..., Any],
    case: dict[str, Any],
    index: int,
    func_a: Callable[..., Any] | None,
) -> dict[str, Any]:
    if task_id in CIRCUIT_STATE_TASK_IDS:
        if func_a is None:
            raise ValueError(f"task {task_id} requires a reference function")
        return evaluate_circuit_state_case(task_id, func_a, func_b, case, index)
    if task_id in {2, 11, 39, 139}:
        if func_a is None:
            raise ValueError(f"task {task_id} requires a reference function")
        return evaluate_state_case(task_id, func_a, func_b, case, index)
    raise ValueError(f"Unsupported task id: {task_id}")


def evaluate_state_case(
    task_id: int,
    func_a: Callable[..., Any],
    func_b: Callable[..., Any],
    case: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    label = case.get("label", f"case_{index}")
    args = tuple(case.get("args", ()))
    kwargs = dict(case.get("kwargs", {}))
    row = base_case_row(label)

    outcome_a = call_and_capture(func_a, clone_value(args), clone_value(kwargs))
    outcome_b = call_and_capture(func_b, clone_value(args), clone_value(kwargs))
    if outcome_a["error"] or outcome_b["error"]:
        row["error"] = combine_errors(outcome_a["error"], outcome_b["error"])
        return row

    try:
        value_a = outcome_a["value"]
        value_b = outcome_b["value"]
        if task_id == 139:
            value_a = reconstruct_schmidt_state(value_a)
            value_b = reconstruct_schmidt_state(value_b)
        metrics = compare_quantum_states(value_a, value_b)
    except Exception:
        row["error"] = f"METRIC ERROR:\n{traceback.format_exc().strip()}"
        return row

    row.update(metrics)
    row["status"] = "PASS" if state_metrics_pass(metrics) else "FAIL"
    return row


def evaluate_circuit_state_case(
    task_id: int,
    func_a: Callable[..., Any],
    func_b: Callable[..., Any],
    case: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    label = case.get("label", f"case_{index}")
    args = tuple(case.get("args", ()))
    kwargs = dict(case.get("kwargs", {}))
    row = base_case_row(label)

    outcome_a = call_and_capture(func_a, clone_value(args), clone_value(kwargs))
    outcome_b = call_and_capture(func_b, clone_value(args), clone_value(kwargs))
    if outcome_a["error"] or outcome_b["error"]:
        row["error"] = combine_errors(outcome_a["error"], outcome_b["error"])
        return row

    try:
        circuit_a = coerce_quantum_circuit(outcome_a["value"])
        circuit_b = coerce_quantum_circuit(outcome_b["value"])
        if task_id in MEASURED_CIRCUIT_TASK_IDS:
            require_measurements(circuit_b)
        value_a = circuit_to_state(task_id, circuit_a, case)
        value_b = circuit_to_state(task_id, circuit_b, case)
        metrics = compare_quantum_states(value_a, value_b)
    except Exception:
        row["error"] = f"METRIC ERROR:\n{traceback.format_exc().strip()}"
        return row

    row.update(metrics)
    row["status"] = "PASS" if state_metrics_pass(metrics) else "FAIL"
    return row


def base_case_row(label: Any) -> dict[str, Any]:
    return {
        "label": label,
        "status": "FAIL",
        "error": None,
        "fidelity": None,
        "trace_distance": None,
        "purity_diff": None,
        "min_metric": None,
        "max_metric": None,
        "failed_items": [],
    }


def coerce_pair(value: Any) -> tuple[Any, Any]:
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError(f"Expected a pair, got {value!r}")
    return value[0], value[1]


def coerce_quantum_circuit(value: Any) -> Any:
    from qiskit import QuantumCircuit

    if isinstance(value, QuantumCircuit):
        return value
    if isinstance(value, (tuple, list)) and value and isinstance(value[0], QuantumCircuit):
        return value[0]
    raise TypeError(f"Expected QuantumCircuit output, got {type(value).__name__}")


def require_measurements(circuit: Any) -> None:
    if not any(instruction.operation.name == "measure" for instruction in circuit.data):
        raise ValueError("Expected returned circuit to contain measurement operations")


def circuit_to_state(task_id: int, circuit: Any, case: dict[str, Any]) -> Any:
    from qiskit.quantum_info import Statevector

    prepared = circuit.copy()
    if task_id in MEASURED_CIRCUIT_TASK_IDS:
        prepared.remove_final_measurements()
    return Statevector.from_instruction(prepared)


def compare_quantum_states(left: Any, right: Any) -> dict[str, float]:
    from qiskit.quantum_info import state_fidelity

    rho = as_density_matrix(left)
    sigma = as_density_matrix(right)
    fidelity = float(state_fidelity(rho, sigma))
    trace_distance_metric = trace_distance(rho, sigma)
    purity_diff_metric = abs(purity_value(rho) - purity_value(sigma))
    return {
        "fidelity": fidelity,
        "trace_distance": trace_distance_metric,
        "purity_diff": purity_diff_metric,
    }


def state_metrics_pass(metrics: dict[str, float]) -> bool:
    return (
        metrics["fidelity"] >= STATE_FIDELITY_MIN
        and metrics["trace_distance"] <= TRACE_DISTANCE_MAX
        and metrics["purity_diff"] <= PURITY_DIFF_MAX
    )


def as_statevector(value: Any) -> Any:
    from qiskit.quantum_info import Statevector

    if isinstance(value, Statevector):
        return value
    return Statevector(value)


def as_density_matrix(value: Any) -> Any:
    from qiskit.quantum_info import DensityMatrix, Statevector

    if isinstance(value, DensityMatrix):
        return value
    if isinstance(value, Statevector):
        return DensityMatrix(value)
    return DensityMatrix(value)


def trace_distance(left: Any, right: Any) -> float:
    rho = as_density_matrix(left).data
    sigma = as_density_matrix(right).data
    delta = rho - sigma
    eigenvalues = np.linalg.eigvalsh(delta)
    return float(0.5 * np.sum(np.abs(eigenvalues)).real)


def purity_value(value: Any) -> float:
    density = as_density_matrix(value).data
    return float(np.trace(density @ density).real)


def reconstruct_schmidt_state(value: Any) -> Any:
    from qiskit.quantum_info import Statevector

    terms = normalize_schmidt_terms(value)
    vector = None
    for coeff, left, right in terms:
        state_left = as_statevector(left)
        state_right = as_statevector(right)
        term = complex(coeff) * state_left.tensor(state_right).data
        vector = term if vector is None else vector + term
    if vector is None:
        raise ValueError("Schmidt decomposition is empty")
    return Statevector(vector)


def normalize_schmidt_terms(value: Any) -> list[tuple[Any, Any, Any]]:
    if isinstance(value, tuple) and len(value) == 2:
        coeffs, subsystems = value
        if isinstance(coeffs, (list, tuple, np.ndarray)) and isinstance(subsystems, (list, tuple)):
            terms = []
            for coeff, pair in zip(coeffs, subsystems):
                left, right = coerce_pair(pair)
                terms.append((coeff, left, right))
            if terms:
                return terms

    if not isinstance(value, (list, tuple)):
        raise TypeError(f"Schmidt decomposition output is not sequence-like: {type(value).__name__}")

    terms = []
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            raise TypeError(f"Schmidt item must be (coeff, vecA, vecB), got {item!r}")
        terms.append((item[0], item[1], item[2]))
    return terms


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
        return {"value": func(*args, **kwargs), "error": None}
    except Exception:
        return {"value": None, "error": traceback.format_exc().strip()}


def clone_value(value: Any) -> Any:
    try:
        return copy.deepcopy(value)
    except Exception:
        return value


def combine_errors(error_a: str | None, error_b: str | None) -> str:
    errors = []
    if error_a:
        errors.append(f"A ERROR:\n{error_a}")
    if error_b:
        errors.append(f"B ERROR:\n{error_b}")
    return "\n".join(errors)


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
        "class_id": 2,
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
        "Qiskit Class 2 raw evaluation report",
        f"dir_a: {details['dir_a']}",
        f"dir_b: {details['dir_b']}",
        (
            "state thresholds: "
            f"fidelity >= {t['state_fidelity_min']}, "
            f"trace_distance <= {t['trace_distance_max']}, "
            f"purity_diff <= {t['purity_diff_max']}"
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
            failed_items = case.get("failed_items") or []
            if failed_items:
                return f"failed_items={len(failed_items)}"
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
    if row.get("fidelity") is not None:
        metric = "state"
        value = (
            f"fid={format_metric(row.get('fidelity'))}, "
            f"td={format_metric(row.get('trace_distance'))}, "
            f"pur={format_metric(row.get('purity_diff'))}"
        )
    else:
        metric = str(row.get("metric_name") or "property")
        value = (
            f"n={row.get('dataset_length')}, "
            f"min={format_metric(row.get('min_metric'))}, "
            f"max={format_metric(row.get('max_metric'))}"
        )
    failed_items = row.get("failed_items") or []
    note = first_line(row.get("error")) if row.get("error") else ""
    if failed_items and not note:
        note = f"failed_items={len(failed_items)}"
    return {
        "code": code,
        "case": str(row["label"]),
        "metric": metric,
        "value": value,
        "status": row["status"],
        "label": raw_label,
        "note": note,
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
            "Statevector",
            "DensityMatrix",
            "state_fidelity",
            "purity",
            "concurrence",
            "entanglement_of_formation",
            "mutual_information",
            "schmidt_decomposition",
        ):
            info["qiskit_symbols"][f"qiskit.quantum_info.{name}"] = hasattr(quantum_info, name)
    except Exception as exc:
        info["qiskit_quantum_info_import_error"] = repr(exc)

    return info


def build_environment_report(info: dict[str, Any] | None = None) -> str:
    env = info or build_environment_info()
    lines = [
        "Qiskit Class 2 raw evaluation environment",
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
    return value.strip().splitlines()[0]
