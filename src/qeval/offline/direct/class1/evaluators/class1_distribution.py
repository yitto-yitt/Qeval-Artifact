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


ROOT = Path(__file__).resolve().parents[1]
LOCAL_STD_DIR = ROOT / "std"
JSD_THRESHOLD = 0.02
TVD_THRESHOLD = 0.05
FIDELITY_THRESHOLD = 0.95
CIRCUIT_SHOTS = 4096
CIRCUIT_SEED = 12345


def thresholds() -> dict[str, float]:
    return {
        "jsd_max": JSD_THRESHOLD,
        "tvd_max": TVD_THRESHOLD,
        "classical_fidelity_min": FIDELITY_THRESHOLD,
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
                evaluate_code_pair(
                    task_id,
                    all_cases[task_id],
                    dir_a,
                    dir_b,
                    sample_index,
                    candidate_path,
                )
            )
    return results


def evaluate_code_pair(
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
        path_a = resolve_reference_code_path(dir_a, task_id)
        path_b = candidate_path or resolve_code_path(dir_b, task_id)
        result["path_a"] = str(path_a)
        result["path_b"] = str(path_b)
        result["candidate_path"] = str(path_b)
        func_a = load_entry_function(path_a, f"raw_a_code{task_id}", spec.entrypoint)
        func_b = load_entry_function(path_b, f"raw_b_code{task_id}_s{sample_index}", spec.entrypoint)
    except Exception:
        result["setup_error"] = traceback.format_exc().strip()
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


def resolve_reference_code_path(root: Path, task_id: int) -> Path:
    try:
        return resolve_code_path(root, task_id)
    except FileNotFoundError:
        if root.expanduser().resolve() != LOCAL_STD_DIR.resolve():
            return resolve_code_path(LOCAL_STD_DIR, task_id)
        raise


def evaluate_case(
    func_a: Callable[..., Any],
    func_b: Callable[..., Any],
    case: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    label = case.get("label", f"case_{index}")
    args = tuple(case.get("args", ()))
    kwargs = dict(case.get("kwargs", {}))
    repeat = int(case.get("repeat", 1))
    row: dict[str, Any] = {
        "label": label,
        "repeat": repeat,
        "jsd": None,
        "tvd": None,
        "classical_fidelity": None,
        "status": "FAIL",
        "error": None,
        "dist_a": None,
        "dist_b": None,
    }

    outcome_a = call_repeated(func_a, args, kwargs, repeat)
    outcome_b = call_repeated(func_b, args, kwargs, repeat)
    if outcome_a["error"] or outcome_b["error"]:
        errors = []
        if outcome_a["error"]:
            errors.append(f"A ERROR:\n{outcome_a['error']}")
        if outcome_b["error"]:
            errors.append(f"B ERROR:\n{outcome_b['error']}")
        row["error"] = "\n".join(errors)
        return row

    try:
        dist_a = outcome_a["value"]
        dist_b = outcome_b["value"]
        metrics = compare_distributions(dist_a, dist_b)
    except Exception:
        row["error"] = f"METRIC ERROR:\n{traceback.format_exc().strip()}"
        return row

    row["dist_a"] = dist_a
    row["dist_b"] = dist_b
    row.update(metrics)
    passed = (
        metrics["jsd"] <= JSD_THRESHOLD
        and metrics["tvd"] <= TVD_THRESHOLD
        and metrics["classical_fidelity"] >= FIDELITY_THRESHOLD
    )
    row["status"] = "PASS" if passed else "FAIL"
    return row


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


def call_repeated(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    repeat: int,
) -> dict[str, Any]:
    if repeat < 1:
        raise ValueError("repeat must be >= 1")

    accumulated: dict[str, float] = {}
    for _ in range(repeat):
        outcome = call_and_capture(func, clone_value(args), clone_value(kwargs))
        if outcome["error"]:
            return outcome
        try:
            dist = to_distribution(outcome["value"])
        except Exception:
            return {"value": None, "error": traceback.format_exc().strip()}
        for key, value in dist.items():
            accumulated[key] = accumulated.get(key, 0.0) + value

    return {
        "value": {key: value / repeat for key, value in accumulated.items()},
        "error": None,
    }


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


def compare_distributions(
    dist_a: dict[str, float],
    dist_b: dict[str, float],
) -> dict[str, float]:
    dist_a, dist_b = canonicalize_distribution_pair(dist_a, dist_b)
    keys = sorted(set(dist_a) | set(dist_b))
    p = normalize_vector([dist_a.get(key, 0.0) for key in keys])
    q = normalize_vector([dist_b.get(key, 0.0) for key in keys])

    tvd = 0.5 * sum(abs(left - right) for left, right in zip(p, q))
    midpoint = [(left + right) / 2.0 for left, right in zip(p, q)]
    jsd = 0.5 * kl_divergence_base2(p, midpoint) + 0.5 * kl_divergence_base2(q, midpoint)
    classical_fidelity = sum(
        math.sqrt(max(left, 0.0) * max(right, 0.0)) for left, right in zip(p, q)
    ) ** 2
    return {
        "jsd": jsd,
        "tvd": tvd,
        "classical_fidelity": classical_fidelity,
    }


def kl_divergence_base2(p: list[float], q: list[float]) -> float:
    total = 0.0
    for left, right in zip(p, q):
        if left == 0.0:
            continue
        if right == 0.0:
            return math.inf
        total += left * math.log(left / right, 2)
    return total


def normalize_vector(values: list[float]) -> list[float]:
    clipped = [max(float(value), 0.0) for value in values]
    total = sum(clipped)
    if total <= 0.0:
        raise ValueError("Distribution has no positive probability mass")
    return [value / total for value in clipped]


def to_distribution(value: Any) -> dict[str, float]:
    candidate = extract_distribution_like(value)
    if candidate is None:
        raise TypeError(f"Return value is not distribution-like: {type(value).__name__}")
    flat = flatten_distribution(candidate)
    total = sum(flat.values())
    if total <= 0.0:
        raise ValueError(f"Distribution has no positive probability mass: {value!r}")
    return {key: probability / total for key, probability in flat.items()}


def extract_distribution_like(value: Any) -> Any | None:
    if isinstance(value, dict):
        return value
    if is_quantum_circuit(value):
        return circuit_to_distribution(value)
    if is_bitstring_sequence(value):
        return bitstrings_to_distribution(value)
    if isinstance(value, tuple):
        if is_numeric_sequence(value):
            return {index: item for index, item in enumerate(value)}
        for item in reversed(value):
            found = extract_distribution_like(item)
            if found is not None:
                return found
    if isinstance(value, list):
        if is_numeric_sequence(value):
            return {index: item for index, item in enumerate(value)}
        for item in reversed(value):
            found = extract_distribution_like(item)
            if found is not None:
                return found
    if hasattr(value, "binary_probabilities"):
        return value.binary_probabilities()
    if hasattr(value, "probabilities_dict"):
        return value.probabilities_dict()
    primitive_dist = primitive_result_to_distribution(value)
    if primitive_dist is not None:
        return primitive_dist
    return None


def is_quantum_circuit(value: Any) -> bool:
    return (
        value.__class__.__name__ == "QuantumCircuit"
        and hasattr(value, "num_qubits")
        and hasattr(value, "count_ops")
    )


def circuit_to_distribution(circuit: Any) -> dict[str, float]:
    if circuit.num_clbits > 0 and circuit.count_ops().get("measure", 0) > 0:
        from qiskit import transpile
        from qiskit_aer import AerSimulator

        simulator = AerSimulator(seed_simulator=CIRCUIT_SEED)
        compiled = transpile(circuit, simulator, seed_transpiler=CIRCUIT_SEED)
        counts = simulator.run(compiled, shots=CIRCUIT_SHOTS).result().get_counts()
        total = sum(counts.values())
        if total <= 0:
            raise ValueError("Circuit simulation produced no counts")
        return {str(key).replace(" ", ""): value / total for key, value in counts.items()}

    from qiskit.quantum_info import Statevector

    return {
        str(key).replace(" ", ""): float(value)
        for key, value in Statevector.from_instruction(circuit).probabilities_dict().items()
    }


def is_bitstring_sequence(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, str) and item.replace(" ", "") for item in value)
        and all(set(item.replace(" ", "")).issubset({"0", "1"}) for item in value)
    )


def bitstrings_to_distribution(value: Any) -> dict[str, float]:
    counts: dict[str, float] = {}
    for item in value:
        key = item.replace(" ", "")
        counts[key] = counts.get(key, 0.0) + 1.0
    return counts


def primitive_result_to_distribution(value: Any) -> Any | None:
    if hasattr(value, "get_counts"):
        try:
            return value.get_counts()
        except Exception:
            pass

    if hasattr(value, "data"):
        found = data_bin_to_distribution(value.data)
        if found is not None:
            return found

    try:
        items = list(value)
    except Exception:
        items = []
    for item in reversed(items):
        found = extract_distribution_like(item)
        if found is not None:
            return found

    return None


def data_bin_to_distribution(data: Any) -> Any | None:
    for name in ("meas", "c", "measure"):
        register = getattr(data, name, None)
        if register is None:
            continue
        found = bit_array_to_distribution(register)
        if found is not None:
            return found
    for name in dir(data):
        if name.startswith("_"):
            continue
        try:
            candidate = getattr(data, name)
        except Exception:
            continue
        found = bit_array_to_distribution(candidate)
        if found is not None:
            return found
    return None


def bit_array_to_distribution(value: Any) -> Any | None:
    for method_name in ("get_counts", "get_int_counts"):
        method = getattr(value, method_name, None)
        if callable(method):
            try:
                return method()
            except Exception:
                pass
    method = getattr(value, "get_bitstrings", None)
    if callable(method):
        try:
            return bitstrings_to_distribution(method())
        except Exception:
            pass
    return None


def flatten_distribution(value: Any, prefix: str = "") -> dict[str, float]:
    if isinstance(value, dict):
        flattened: dict[str, float] = {}
        for key, item in value.items():
            child_prefix = join_key(prefix, stable_key(key))
            if is_number(item):
                flattened[child_prefix] = flattened.get(child_prefix, 0.0) + float(item)
            else:
                for child_key, child_value in flatten_distribution(item, child_prefix).items():
                    flattened[child_key] = flattened.get(child_key, 0.0) + child_value
        return flattened
    if is_numeric_sequence(value):
        return {join_key(prefix, stable_key(index)): float(item) for index, item in enumerate(value)}
    if is_number(value):
        return {prefix or "value": float(value)}
    raise TypeError(f"Distribution leaf is not numeric: {value!r}")


def canonicalize_distribution_pair(
    dist_a: dict[str, float],
    dist_b: dict[str, float],
) -> tuple[dict[str, float], dict[str, float]]:
    keys = list(dist_a) + list(dist_b)
    widths: dict[str, int] = {}
    for key in keys:
        parsed = parse_binary_like_key(key)
        if parsed is None:
            continue
        prefix, _, width = parsed
        widths[prefix] = max(widths.get(prefix, 1), width)
    return (
        canonicalize_distribution_keys(dist_a, widths),
        canonicalize_distribution_keys(dist_b, widths),
    )


def canonicalize_distribution_keys(dist: dict[str, float], widths: dict[str, int]) -> dict[str, float]:
    canonical: dict[str, float] = {}
    for key, value in dist.items():
        parsed = parse_binary_like_key(key)
        if parsed is None:
            canonical_key = key
        else:
            prefix, number, width = parsed
            final_width = max(widths.get(prefix, width), 1)
            rendered = format(number, f"0{final_width}b")
            canonical_key = join_key(prefix, rendered) if prefix else rendered
        canonical[canonical_key] = canonical.get(canonical_key, 0.0) + value
    return canonical


def parse_binary_like_key(key: str) -> tuple[str, int, int] | None:
    prefix, _, tail = key.rpartition(".")
    if tail.startswith("int:"):
        raw = tail[4:]
        if raw.isdecimal():
            number = int(raw)
            return prefix, number, max(1, number.bit_length())
    compact = tail.replace(" ", "")
    if compact and all(char in "01" for char in compact):
        return prefix, int(compact, 2), len(compact)
    return None


def is_numeric_sequence(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and bool(value) and all(is_number(item) for item in value)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def stable_key(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return f"int:{value}"
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def join_key(prefix: str, key: str) -> str:
    return f"{prefix}.{key}" if prefix else key


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

    summary = build_summary_from_results(results)
    return {
        "mode": "raw",
        "dir_a": str(dir_a),
        "dir_b": str(dir_b),
        "thresholds": thresholds(),
        "environment": build_environment_info(),
        "summary": summary,
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
        details.get("report_title", "Qiskit Class 1 raw evaluation report"),
        f"dir_a: {details['dir_a']}",
        f"dir_b: {details['dir_b']}",
        (
            "thresholds: "
            f"jsd <= {t['jsd_max']}, "
            f"tvd <= {t['tvd_max']}, "
            f"classical_fidelity >= {t['classical_fidelity_min']}"
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
        import qiskit

        info["qiskit_symbols"]["qiskit.Aer"] = hasattr(qiskit, "Aer")
        info["qiskit_symbols"]["qiskit.execute"] = hasattr(qiskit, "execute")
    except Exception as exc:
        info["qiskit_import_error"] = repr(exc)

    try:
        import qiskit.primitives as primitives

        for name in ("Sampler", "StatevectorSampler", "BackendSamplerV2", "StatevectorEstimator"):
            info["qiskit_symbols"][f"qiskit.primitives.{name}"] = hasattr(primitives, name)
    except Exception as exc:
        info["qiskit_primitives_import_error"] = repr(exc)

    return info


def build_environment_report(info: dict[str, Any] | None = None) -> str:
    env = info or build_environment_info()
    lines = [
        "Qiskit Class 1 raw evaluation environment",
        f"python: {env.get('python')}",
        f"platform: {env.get('platform')}",
    ]
    for package, version in env.get("packages", {}).items():
        lines.append(f"{package}: {version or 'not installed'}")
    for symbol, exists in env.get("qiskit_symbols", {}).items():
        lines.append(f"{symbol} exists: {exists}")
    if "qiskit_import_error" in env:
        lines.append(f"qiskit import error: {env['qiskit_import_error']}")
    if "qiskit_primitives_import_error" in env:
        lines.append(f"qiskit.primitives import error: {env['qiskit_primitives_import_error']}")
    return "\n".join(lines) + "\n"


def max_width(rows: list[dict[str, str]], key: str, header: str) -> int:
    return max([len(header), *(len(str(row[key])) for row in rows)])


def format_metric(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"{float(value):.12g}"


def format_rate(value: Any) -> str:
    if value in ("", None):
        return ""
    return f"{float(value):.2f}"


def first_line(value: str | None) -> str:
    if not value:
        return ""
    return value.strip().splitlines()[0]
