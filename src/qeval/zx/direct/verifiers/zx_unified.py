from __future__ import annotations

import argparse
import ast
import contextlib
import csv
import importlib.util
import inspect
import io
import json
import re
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HELPERS_ROOT = PROJECT_ROOT / "helpers"
for helper_path in (PROJECT_ROOT, HELPERS_ROOT):
    text = str(helper_path)
    if text not in sys.path:
        sys.path.append(text)

from framework_cases import build_cases
from qiskit_case_converters import convert_args_for_framework, convert_kwargs_for_framework


SOURCE_DEFAULTS = {
    "type1": {
        "dir_a": "class1/codes",
        "dir_b": "Qclass1",
        "pattern_a": "ncode{idx}.py",
        "pattern_b": "llmQpanda{idx}.py",
        "out": "type1-result.md",
        "out_dir_report": "type1-report.md",
        "framework_choices": ["auto", "qiskit", "cirq", "Qpanda3", "pennylane"],
    },
    "type2": {
        "dir_a": "class2/codes",
        "dir_b": "Qclass2",
        "pattern_a": "code{idx}.py",
        "pattern_b": "llmQpanda{idx}.py",
        "out": "type2-result.md",
        "out_dir_report": "type2-report.md",
        "framework_choices": ["auto", "qiskit", "cirq", "Qpanda3", "pennylane"],
    },
    "type3": {
        "dir_a": "class3/codes",
        "dir_b": "class3/llms",
        "pattern_a": "code{idx}.py",
        "pattern_b": "llm{idx}.py",
        "out": "resulttype3.md",
        "out_dir_report": "type3-report.md",
        "framework_choices": ["auto", "qiskit", "cirq", "Qpanda3", "pennylane"],
    },
}

SCRIPT_FILES = {
    "type1": "type1_verify.py",
    "type2": "type2_verify.py",
    "type3": "type3_verify.py",
}

STATUS_EN = {
    "EQUIVALENT": "Equivalent",
    "NOT_PROVED": "Not Proved",
    "MISSING": "Missing",
}

ZX_RESULT_STATES = {"EQUIVALENT", "NOT_PROVED"}


def normalize_zx_status(status: Any) -> str:
    text = str(status or "").upper()
    return "EQUIVALENT" if text == "EQUIVALENT" else "NOT_PROVED"


@dataclass
class RunContext:
    source_class: str
    base: Path
    dir_a: Path
    dir_b: Path
    pattern_a: str
    pattern_b: str
    framework_a: str | None
    framework_b: str | None
    out_path: Path
    csv_path: Path
    audit_path: Path
    manifest_path: Path


def legacy_main(source_class: str, legacy_globals: dict[str, Any], argv: list[str] | None = None) -> None:
    base = Path(str(legacy_globals.get("__file__", __file__))).resolve().parent
    modules = LegacyModules(base, source_class, legacy_globals)
    ctx, indices = parse_legacy_args(source_class, base, argv)
    manifest = load_manifest(ctx.manifest_path)
    add_import_paths(ctx)

    rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for idx in indices:
        idx_rows, idx_audits = run_index_cases(ctx, modules, manifest, idx)
        rows.extend(idx_rows)
        audit_rows.extend(idx_audits)
        for row in idx_rows:
            case = f" [{row.get('case', '')}]" if row.get("case") else ""
            print(f"[{idx:>3}]{case}  {row['result']:<14}  {row['notes'][:180]}")

    write_reports(ctx, rows, audit_rows)
    print(f"\nReport written to {ctx.out_path}")
    print(f"CSV written to {ctx.csv_path}")
    print(f"Routing audit written to {ctx.audit_path}")


def parse_legacy_args(source_class: str, base: Path, argv: list[str] | None) -> tuple[RunContext, list[int]]:
    defaults = SOURCE_DEFAULTS[source_class]
    parser = argparse.ArgumentParser(
        description=f"Unified ZX verifier compatibility entry ({source_class})"
    )
    parser.add_argument("--dir-a", default=defaults["dir_a"])
    parser.add_argument("--dir-b", default=defaults["dir_b"])
    parser.add_argument("--pattern-a", default=defaults["pattern_a"])
    parser.add_argument("--pattern-b", default=defaults["pattern_b"])
    parser.add_argument("--framework-a", choices=defaults["framework_choices"], default="auto")
    parser.add_argument("--framework-b", choices=defaults["framework_choices"], default="auto")
    parser.add_argument("--indices", default="all")
    parser.add_argument("--out", default=None)
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--csv-out", default=None)
    parser.add_argument("--audit-out", default=None)
    parser.add_argument("--manifest", default="routing-manifest.json")
    parser.add_argument("--path-add", action="append", default=[])
    args = parser.parse_args(argv)

    dir_a = resolve_path(base, args.dir_a)
    dir_b = resolve_path(base, args.dir_b)
    out_dir = resolve_path(base, args.out_dir) if args.out_dir else None
    if out_dir:
        out_path = resolve_output_file(
            base,
            out_dir,
            args.out,
            defaults["out_dir_report"],
            filename_only=True,
        )
        csv_path = resolve_output_file(
            base,
            out_dir,
            args.csv_out,
            out_path.with_suffix(".csv").name,
        )
        audit_path = resolve_output_file(
            base,
            out_dir,
            args.audit_out,
            "routing-audit.jsonl",
        )
    else:
        out_path = resolve_path(base, args.out or defaults["out"])
        csv_path = resolve_path(base, args.csv_out) if args.csv_out else out_path.with_suffix(".csv")
        audit_path = resolve_path(base, args.audit_out) if args.audit_out else out_path.with_name("routing-audit.jsonl")
    manifest_path = resolve_path(base, args.manifest)

    if not dir_a.is_dir():
        parser.error(f"--dir-a is not a valid directory: {dir_a}")
    if not dir_b.is_dir():
        parser.error(f"--dir-b is not a valid directory: {dir_b}")

    extra_paths = [resolve_path(base, p) for p in args.path_add]
    for p in [base, dir_a.parent, dir_b.parent, dir_a, dir_b, *extra_paths]:
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)

    if not args.indices or args.indices.lower() in ("all", "*"):
        indices = discover_paired_indices(dir_a, args.pattern_a, dir_b, args.pattern_b)
        if not indices:
            parser.error("no paired files found matching pattern-a and pattern-b")
    else:
        indices = parse_indices(args.indices)

    ctx = RunContext(
        source_class=source_class,
        base=base,
        dir_a=dir_a,
        dir_b=dir_b,
        pattern_a=args.pattern_a,
        pattern_b=args.pattern_b,
        framework_a=None if args.framework_a == "auto" else args.framework_a.lower(),
        framework_b=None if args.framework_b == "auto" else args.framework_b.lower(),
        out_path=out_path,
        csv_path=csv_path,
        audit_path=audit_path,
        manifest_path=manifest_path,
    )
    return ctx, indices


def add_import_paths(ctx: RunContext) -> None:
    for p in [ctx.base, ctx.dir_a.parent, ctx.dir_b.parent, ctx.dir_a, ctx.dir_b]:
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)


def resolve_path(base: Path, path_like: str | None) -> Path:
    if not path_like:
        return base
    p = Path(path_like)
    return p if p.is_absolute() else (base / p).resolve()


def resolve_output_file(
    base: Path,
    out_dir: Path,
    value: str | None,
    default_name: str,
    filename_only: bool = False,
) -> Path:
    if not value:
        return out_dir / default_name
    p = Path(value)
    if filename_only:
        return out_dir / p.name
    if p.is_absolute():
        return p
    return out_dir / p


def parse_indices(spec: str) -> list[int]:
    parsed: list[int] = []
    for raw in spec.split(","):
        token = raw.strip()
        if not token:
            continue
        if "-" in token:
            a, b = token.split("-", 1)
            start, end = int(a), int(b)
            if end < start:
                start, end = end, start
            parsed.extend(range(start, end + 1))
        else:
            parsed.append(int(token))
    return sorted(set(parsed))


def compile_idx_pattern(pattern: str) -> re.Pattern[str]:
    if "{idx}" not in pattern:
        raise ValueError("pattern must contain {idx}")
    escaped = re.escape(pattern).replace(re.escape("{idx}"), r"(\d+)")
    return re.compile(rf"^{escaped}$")


def discover_indices(directory: Path, pattern: str) -> set[int]:
    rx = compile_idx_pattern(pattern)
    found: set[int] = set()
    for child in directory.iterdir():
        if not child.is_file():
            continue
        m = rx.match(child.name)
        if m:
            found.add(int(m.group(1)))
    return found


def discover_paired_indices(dir_a: Path, pattern_a: str, dir_b: Path, pattern_b: str) -> list[int]:
    return sorted(discover_indices(dir_a, pattern_a) & discover_indices(dir_b, pattern_b))


def load_manifest(path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("overrides", data if isinstance(data, list) else [])
    manifest: dict[tuple[str, int], dict[str, Any]] = {}
    for entry in entries:
        manifest[(str(entry["source_class"]), int(entry["task_id"]))] = dict(entry)
    return manifest


class LegacyModules:
    def __init__(self, base: Path, current_source: str, current_globals: dict[str, Any]):
        self.base = base
        self.current_source = current_source
        self.current_module = types.SimpleNamespace(**current_globals)
        self._cache: dict[str, Any] = {current_source: self.current_module}

    def get(self, source_class: str) -> Any:
        if source_class in self._cache:
            return self._cache[source_class]
        script = self.base / SCRIPT_FILES[source_class]
        name = f"_zx_legacy_{source_class}_{abs(hash(str(script)))}"
        spec = importlib.util.spec_from_file_location(name, script)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load legacy module: {script}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        self._cache[source_class] = mod
        return mod


def run_index(
    ctx: RunContext,
    modules: LegacyModules,
    manifest: dict[tuple[str, int], dict[str, Any]],
    idx: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    rows, audits = run_index_cases(ctx, modules, manifest, idx)
    return rows[0], audits[0]


def run_index_cases(
    ctx: RunContext,
    modules: LegacyModules,
    manifest: dict[tuple[str, int], dict[str, Any]],
    idx: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    override = manifest.get((ctx.source_class, idx), {})
    cases = expand_override_cases(ctx.source_class, override, idx)
    rows: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    for case_label, case_override in cases:
        row, audit = run_index_one_case(ctx, modules, manifest, idx, case_override, case_label)
        rows.append(row)
        audits.append(audit)
    return rows, audits


def expand_override_cases(source_class: str, override: dict[str, Any], idx: int) -> list[tuple[str | None, dict[str, Any]]]:
    arg_cases = override.get("arg_cases") if override else None
    if not arg_cases and should_use_raw_cases(source_class, override):
        arg_cases = build_raw_arg_cases(idx)
    if not arg_cases:
        return [(None, override)]
    expanded: list[tuple[str | None, dict[str, Any]]] = []
    for item in arg_cases:
        case_override = dict(override)
        case_override.pop("arg_cases", None)
        case_override.pop("arg_spec", None)
        case_override.pop("arg_candidates", None)
        if item.get("_raw_case"):
            case_override["raw_case_args"] = list(item.get("args", ()))
            case_override["raw_case_kwargs"] = dict(item.get("kwargs", {}))
            if "compare_to_input" in item and item.get("compare_to_input") is not None:
                case_override["compare_to_input"] = item.get("compare_to_input")
            if "compare_modified_input" in item and item.get("compare_modified_input") is not None:
                case_override["compare_modified_input"] = item.get("compare_modified_input")
        elif "arg_candidates" in item:
            case_override["arg_candidates"] = item["arg_candidates"]
        elif "args" in item:
            if isinstance(item["args"], dict):
                case_override["arg_spec"] = item["args"]
            else:
                case_override["arg_candidates"] = [item["args"]]
        else:
            case_override["arg_spec"] = item.get("arg_spec", {})
        label = str(item.get("label", ""))
        case_override["case_label"] = label
        expanded.append((label, case_override))
    return expanded or [(None, override)]


def should_use_raw_cases(source_class: str, override: dict[str, Any]) -> bool:
    mode = str(override.get("verification_mode", source_class)).lower() if override else source_class
    if mode != "type3":
        return False
    if override.get("arg_cases"):
        return False
    extractor = str(override.get("extractor", "auto"))
    return extractor in {"auto", "first_comparable_circuit", "all_comparable_circuits"}


def build_raw_arg_cases(idx: int) -> list[dict[str, Any]]:
    all_cases = build_cases()
    raw_cases = all_cases.get(idx, [])
    built: list[dict[str, Any]] = []
    for case in raw_cases:
        built.append(
            {
                "_raw_case": True,
                "label": case.get("label", ""),
                "args": list(case.get("args", ())),
                "kwargs": dict(case.get("kwargs", {})),
                "compare_to_input": case.get("compare_to_input"),
                "compare_modified_input": case.get("compare_modified_input"),
            }
        )
    return built


def framework_name_for_conversion(file_path: Path) -> str | None:
    try:
        source = file_path.read_text(encoding="utf-8-sig", errors="replace")[:300]
    except Exception:
        return None
    match = re.search(r"EVAL_META:.*?\bframework\s*=\s*([A-Za-z0-9_]+)", source)
    if not match:
        return None
    framework = match.group(1).strip().lower()
    if framework == "qpanda":
        return "qpanda"
    if framework == "cirq":
        return "cirq"
    if framework == "pennylane":
        return "pennylane"
    if framework == "qiskit":
        return "qiskit"
    return None


_PENNYLANE_CONVERTER: tuple[Any, Any] | None = None


def _load_pennylane_converters() -> tuple[Any, Any] | None:
    global _PENNYLANE_CONVERTER
    if _PENNYLANE_CONVERTER is not None:
        return _PENNYLANE_CONVERTER

    converter_path = (
        Path(__file__).resolve().parents[4]
        / "cross_pennylane"
        / "cross_language3_translate_eval"
        / "cross_language3_translate_eval"
        / "main_pennylane.py"
    )
    if not converter_path.exists():
        _PENNYLANE_CONVERTER = None
        return None

    spec = importlib.util.spec_from_file_location("_zx_pennylane_main", converter_path)
    if spec is None or spec.loader is None:
        _PENNYLANE_CONVERTER = None
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        spec.loader.exec_module(module)
    convert_args = getattr(module, "convert_args_for_framework", None)
    convert_kwargs = getattr(module, "convert_kwargs_for_framework", None)
    if convert_args is None or convert_kwargs is None:
        convert_value = getattr(module, "convert_value_for_framework")

        def convert_args(args: tuple[Any, ...], framework: str, task_id: int) -> tuple[Any, ...]:
            return tuple(convert_value(value, framework, task_id) for value in args)

        def convert_kwargs(kwargs: dict[str, Any], framework: str, task_id: int) -> dict[str, Any]:
            return {key: convert_value(value, framework, task_id) for key, value in kwargs.items()}

    _PENNYLANE_CONVERTER = (convert_args, convert_kwargs)
    return _PENNYLANE_CONVERTER


def convert_args_for_target_framework(args: tuple[Any, ...], framework: str, task_id: int) -> tuple[Any, ...]:
    if framework == "pennylane":
        converters = _load_pennylane_converters()
        if converters is not None:
            return tuple(converters[0](args, framework, task_id))
        return tuple(args)
    return tuple(convert_args_for_framework(args, framework, task_id))


def build_case_arg_candidates(
    file_a: Path,
    file_b: Path,
    idx: int,
    fn_a: str | None,
    fn_b: str | None,
    override: dict[str, Any],
) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    payload = override.get("arg_candidates") or override.get("arg_spec")
    if payload:
        return (
            build_arg_candidates_from_manifest(payload, file_a, fn_a),
            build_arg_candidates_from_manifest(payload, file_b, fn_b),
        )

    case_args = override.get("raw_case_args")
    case_kwargs = override.get("raw_case_kwargs") or {}
    if case_args is None:
        return [], []

    args_a = [tuple(case_args)]
    framework_b = framework_name_for_conversion(file_b)
    if framework_b in {"cirq", "qpanda", "pennylane"}:
        converted_args = convert_args_for_target_framework(tuple(case_args), framework_b, idx)
    else:
        converted_args = tuple(case_args)

    return args_a, [tuple(converted_args)]


def run_index_one_case(
    ctx: RunContext,
    modules: LegacyModules,
    manifest: dict[tuple[str, int], dict[str, Any]],
    idx: int,
    override: dict[str, Any],
    case_label: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    file_a = ctx.dir_a / ctx.pattern_a.format(idx=idx)
    file_b = ctx.dir_b / ctx.pattern_b.format(idx=idx)
    route = route_for(ctx.source_class, idx, file_a, override)

    audit = {
        "source_class": ctx.source_class,
        "task_id": idx,
        "case": case_label or "",
        "verification_mode": route["verification_mode"],
        "route_reason": route["route_reason"],
        "override_used": bool(override),
        "entry_fn": None,
        "status": "PENDING",
        "capture_source": "",
    }

    if not file_a.exists() or not file_b.exists():
        missing = []
        if not file_a.exists():
            missing.append(f"A:{file_a}")
        if not file_b.exists():
            missing.append(f"B:{file_b}")
        row = {
            "index": idx,
            "case": case_label or "",
            "result": "NOT_PROVED",
            "zx_equivalent": False,
            "notes": "not proved: " + "; ".join(missing),
            "capture_source": "",
        }
        audit["status"] = row["result"]
        return row, audit

    try:
        result = dispatch_pair(ctx, modules, idx, file_a, file_b, route, override, audit)
    except Exception as exc:
        result = {"idx": idx, "status": "NOT_PROVED", "detail": f"not proved: {exc}"}

    status = normalize_zx_status(result.get("status", "NOT_PROVED"))
    row = {
        "index": idx,
        "case": result.get("case", case_label or ""),
        "result": status,
        "zx_equivalent": status == "EQUIVALENT",
        "notes": result.get("detail", ""),
        "capture_source": result.get("capture_source", ""),
    }
    audit["status"] = row["result"]
    audit["case"] = row["case"]
    audit["capture_source"] = row["capture_source"]
    return row, audit


def route_for(source_class: str, idx: int, file_a: Path, override: dict[str, Any]) -> dict[str, str]:
    if override:
        expected = str(override.get("expected_outcome", "")).upper()
        mode = str(override.get("verification_mode", source_class)).lower()
        if expected == "NOT_APPLICABLE":
            mode = "not_applicable"
        return {
            "verification_mode": mode,
            "route_reason": str(override.get("reason", "manifest override")),
        }

    meta_class = read_eval_meta_class(file_a)
    return {
        "verification_mode": source_class if meta_class is None else f"type{meta_class}",
        "route_reason": "source_class fallback",
    }


def read_eval_meta_class(path: Path) -> int | None:
    try:
        head = path.read_text(encoding="utf-8-sig", errors="replace")[:300]
    except Exception:
        return None
    m = re.search(r"EVAL_META:.*?\bclass\s*=\s*(\d+)", head)
    return int(m.group(1)) if m else None


def dispatch_pair(
    ctx: RunContext,
    modules: LegacyModules,
    idx: int,
    file_a: Path,
    file_b: Path,
    route: dict[str, str],
    override: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    mode = route["verification_mode"]
    expected = str(override.get("expected_outcome", "")).upper()
    if mode == "not_applicable" or expected == "NOT_APPLICABLE":
        return {"idx": idx, "status": "NOT_APPLICABLE", "detail": route["route_reason"]}

    extractor = str(override.get("extractor", "auto"))
    if extractor == "capture_operator_from_circuit_input":
        return run_operator_from_circuit_capture(ctx, modules, idx, file_a, file_b, override, audit)

    if extractor == "all_comparable_circuits":
        return run_type3_all_comparable_circuits(ctx, modules, idx, file_a, file_b, override, audit)

    if extractor == "capture_state_constructor_input":
        result = run_state_constructor_capture(ctx, modules, idx, file_a, file_b, override, audit)
        if result["status"] == "CAPTURE_FAIL" and expected in {"ZX_IF_CAPTURED_ELSE_NOT_APPLICABLE", "NOT_APPLICABLE"}:
            result["status"] = "NOT_APPLICABLE"
        return result

    if mode == "type3":
        if (
            extractor != "auto"
            or override.get("arg_spec")
            or override.get("arg_candidates")
            or override.get("raw_case_args") is not None
        ):
            return run_type3_special(ctx, modules, idx, file_a, file_b, override, audit)
        t3 = modules.get("type3")
        return t3.run_pair_type3(idx, str(file_a), str(file_b), ctx.framework_a, ctx.framework_b)

    if mode in {"type1", "type2"}:
        mod = modules.get(mode)
        prog_a = prog_b = None
        if override.get("entry_fn_a") or override.get("entry_fn_b") or override.get("arg_spec") or override.get("arg_candidates"):
            prog_a, prog_b = build_legacy_prog_dict(mod, idx, file_a, file_b, override)
            audit["entry_fn"] = prog_a.get(idx, (None,))[0] if prog_a else None
        return mod.run_pair_flexible(
            idx,
            str(file_a),
            str(file_b),
            prog_a=prog_a,
            prog_b=prog_b,
            framework_a=ctx.framework_a,
            framework_b=ctx.framework_b,
        )

    return {"idx": idx, "status": "UNSUPPORTED", "detail": f"unknown verification_mode={mode}"}


def build_legacy_prog_dict(
    mod: Any,
    idx: int,
    file_a: Path,
    file_b: Path,
    override: dict[str, Any],
) -> tuple[dict[int, Any], dict[int, Any]]:
    entry_a = override.get("entry_fn_a") or infer_first_function(file_a)
    entry_b = override.get("entry_fn_b") or infer_matching_function(file_b, entry_a)
    arg_payload = override.get("arg_candidates") or override.get("arg_spec")
    case_label = override.get("case_label", "")
    if hasattr(mod, "_as_arg_spec_candidates"):
        specs = build_arg_candidates_from_manifest(arg_payload, file_a, entry_a)
    else:
        specs = build_arg_candidates_from_manifest(arg_payload, file_a, entry_a)
        specs = specs[0] if specs else tuple()
    return {idx: (entry_a, specs, case_label)}, {idx: (entry_b, specs, case_label)}


def run_type3_special(
    ctx: RunContext,
    modules: LegacyModules,
    idx: int,
    file_a: Path,
    file_b: Path,
    override: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    t3 = modules.get("type3")
    fn_a = override.get("entry_fn_a") or t3.find_entry_fn_codes(file_a)
    fn_b = override.get("entry_fn_b") or t3.find_llm_fn(file_b, fn_a) or fn_a
    audit["entry_fn"] = fn_a
    case_label = override.get("case_label", "")
    if not fn_a or not fn_b:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": f"A: no comparable circuit captured; fn={fn_a or ''}; case={case_label}"
            if case_label else f"A: no comparable circuit captured; fn={fn_a or ''}",
            "capture_source": "",
        }

    extractor = str(override.get("extractor", "auto"))
    args_a, args_b = build_case_arg_candidates(file_a, file_b, idx, fn_a, fn_b, override)
    if not args_a:
        args_a = t3.build_arg_candidates(file_a, fn_a)
    if not args_b:
        args_b = t3.build_arg_candidates(file_b, fn_b)
    for cand in args_a:
        if cand not in args_b:
            args_b.append(cand)

    circ_a, err_a = call_and_extract_circuit(t3, file_a, fn_a, args_a, extractor, "A", case_label)
    if circ_a is None:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": err_a or f"A: no comparable circuit captured; fn={fn_a}",
            "capture_source": "",
        }
    circ_b, err_b = call_and_extract_circuit(t3, file_b, fn_b, args_b, extractor, "B", case_label)
    if circ_b is None:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": err_b or f"B: no comparable circuit captured; fn={fn_b}",
            "capture_source": "A:return_value; B:",
        }

    return compare_captured_circuits(
        t3,
        idx,
        circ_a,
        circ_b,
        f"fn_a={fn_a}, fn_b={fn_b}, extractor={extractor}",
        case_label=case_label,
        capture_source="A:return_value; B:return_value",
    )


def call_and_extract_circuit(
    t3: Any,
    file_path: Path,
    fn_name: str,
    candidates: list[tuple[Any, ...]],
    extractor: str,
    side: str = "",
    case_label: str | None = None,
) -> tuple[tuple[str, Any] | None, str]:
    mod_name = f"_zx_call_{file_path.stem}_{abs(hash((str(file_path), fn_name)))}"
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    try:
        mod = t3._load_module(str(file_path), mod_name)
    except Exception as exc:
        return None, f"load error: {exc}"
    fn = getattr(mod, fn_name, None)
    if fn is None:
        return None, f"function `{fn_name}` not found"

    last_err = "no candidates tried"
    for candidate in candidates or [tuple()]:
        try:
            args = clone_candidate(candidate)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                result = fn(*args)
            circ = extract_circuit_from_result(t3, result, extractor)
            if circ is None and extractor == "inplace_circuit_arg":
                for arg in args:
                    circ = extract_circuit_from_result(t3, arg, "auto")
                    if circ is not None:
                        break
            if circ is not None:
                return circ, ""
            last_err = f"returned {type(result).__name__}, no circuit extracted"
        except Exception as exc:
            last_err = str(exc)
    suffix = f"; case={case_label}" if case_label else ""
    return None, f"{side}: no comparable circuit captured; fn={fn_name}{suffix}; last={last_err}"


def clone_candidate(candidate: tuple[Any, ...]) -> tuple[Any, ...]:
    cloned = []
    for item in candidate:
        if hasattr(item, "copy"):
            try:
                cloned.append(item.copy())
                continue
            except Exception:
                pass
        cloned.append(item)
    return tuple(cloned)


def extract_circuit_from_result(t3: Any, result: Any, extractor: str) -> tuple[str, Any] | None:
    try:
        qc = t3.extract_returned_circuit(result)
        if qc is not None:
            return qc
    except Exception:
        pass

    try:
        if isinstance(result, (tuple, list)):
            for item in result:
                qc = extract_circuit_from_result(t3, item, extractor)
                if qc is not None:
                    return qc
    except Exception:
        pass

    if result is None:
        return None

    if extractor in {"dag_to_circuit", "auto", "first_comparable_circuit"}:
        try:
            from qiskit.converters import dag_to_circuit
            from qiskit.dagcircuit import DAGCircuit
            if isinstance(result, DAGCircuit):
                return ("qiskit", dag_to_circuit(result))
        except Exception:
            pass

    if extractor in {"to_circuit", "auto", "first_comparable_circuit"}:
        method = getattr(result, "to_circuit", None)
        if callable(method):
            try:
                converted = method()
                extracted = t3.extract_returned_circuit(converted)
                if extracted is not None:
                    return extracted
            except Exception:
                pass

    if extractor in {"instruction_to_circuit", "auto", "first_comparable_circuit"}:
        try:
            from qiskit import QuantumCircuit
            from qiskit.circuit import Gate, Instruction
            if isinstance(result, (Gate, Instruction)):
                qc = QuantumCircuit(result.num_qubits, getattr(result, "num_clbits", 0))
                qc.append(result, list(range(result.num_qubits)), list(range(getattr(result, "num_clbits", 0))))
                return ("qiskit", qc)
        except Exception:
            pass

    return None


def extract_all_circuits_from_result(t3: Any, result: Any, extractor: str) -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []

    if isinstance(result, (tuple, list)):
        for item in result:
            found.extend(extract_all_circuits_from_result(t3, item, extractor))
        return found

    if isinstance(result, dict):
        for item in result.values():
            found.extend(extract_all_circuits_from_result(t3, item, extractor))
        return found

    single = extract_circuit_from_result(t3, result, extractor)
    if single is not None:
        found.append(single)
    return found


def run_operator_from_circuit_capture(
    ctx: RunContext,
    modules: LegacyModules,
    idx: int,
    file_a: Path,
    file_b: Path,
    override: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    t3 = modules.get("type3")
    fn_a = override.get("entry_fn_a") or infer_first_function(file_a)
    fn_b = override.get("entry_fn_b") or infer_matching_function(file_b, fn_a)
    audit["entry_fn"] = fn_a
    case_label = override.get("case_label", "")

    args_a, args_b = build_case_arg_candidates(file_a, file_b, idx, fn_a, fn_b, override)
    if not args_a:
        args_a = [tuple()]
    if not args_b:
        args_b = list(args_a)

    circ_a, err_a = capture_operator_from_circuit_input(t3, file_a, fn_a, args_a)
    if circ_a is None:
        return {"idx": idx, "case": case_label, "status": "NOT_PROVED", "detail": f"not proved: {err_a}", "capture_source": ""}
    circ_b, err_b = capture_operator_from_circuit_input(t3, file_b, fn_b, args_b)
    if circ_b is None:
        return {"idx": idx, "case": case_label, "status": "NOT_PROVED", "detail": f"not proved: {err_b}", "capture_source": "A:operator_input; B:"}

    return compare_captured_circuits(
        t3,
        idx,
        circ_a,
        circ_b,
        f"fn_a={fn_a}, fn_b={fn_b}, extractor=capture_operator_from_circuit_input",
        case_label=case_label,
        capture_source="A:operator_input; B:operator_input",
    )


def run_type3_all_comparable_circuits(
    ctx: RunContext,
    modules: LegacyModules,
    idx: int,
    file_a: Path,
    file_b: Path,
    override: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    t3 = modules.get("type3")
    fn_a = override.get("entry_fn_a") or t3.find_entry_fn_codes(file_a)
    fn_b = override.get("entry_fn_b") or t3.find_llm_fn(file_b, fn_a) or fn_a
    audit["entry_fn"] = fn_a
    case_label = override.get("case_label", "")
    if not fn_a or not fn_b:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": f"not proved: A: no comparable circuit captured; fn={fn_a or ''}; case={case_label}"
            if case_label else f"A: no comparable circuit captured; fn={fn_a or ''}",
            "capture_source": "",
        }

    extractor = str(override.get("extractor", "all_comparable_circuits"))
    args_a, args_b = build_case_arg_candidates(file_a, file_b, idx, fn_a, fn_b, override)
    if not args_a:
        args_a = t3.build_arg_candidates(file_a, fn_a)
    if not args_b:
        args_b = t3.build_arg_candidates(file_b, fn_b)
    for cand in args_a:
        if cand not in args_b:
            args_b.append(cand)

    compare_to_input = override.get("compare_to_input")
    compare_input_index = int(compare_to_input) if compare_to_input is not None else None
    if compare_input_index is not None:
        circ_a, err_a = capture_input_circuit_from_candidates(args_a, compare_input_index)
        capture_source_a = f"A:arg[{compare_input_index}]"
        if circ_a is None:
            return {
                "idx": idx,
                "case": case_label,
                "status": "NOT_PROVED",
                "detail": f"not proved: {err_a or f'A: no comparable input circuit captured; arg_index={compare_input_index}'}",
                "capture_source": "",
            }
    else:
        circ_a, err_a = call_and_extract_circuit(t3, file_a, fn_a, args_a, extractor, "A", case_label)
        capture_source_a = "A:return_value"
        if circ_a is None:
            return {
                "idx": idx,
                "case": case_label,
                "status": "NOT_PROVED",
                "detail": f"not proved: {err_a or f'A: no comparable circuit captured; fn={fn_a}'}",
                "capture_source": "",
            }

    all_b, err_b = call_and_extract_all_circuits(t3, file_b, fn_b, args_b, extractor, "B", case_label)
    if not all_b:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": f"not proved: {err_b or f'B: no comparable circuit captured; fn={fn_b}'}",
            "capture_source": f"{capture_source_a}; B:",
        }

    failures: list[str] = []
    compared = 0
    for seq_index, circ_b in enumerate(all_b):
        result = compare_captured_circuits(
            t3,
            idx,
            circ_a,
            circ_b,
            f"fn_a={fn_a}, fn_b={fn_b}, extractor={extractor}, seq_index={seq_index}",
            case_label=case_label,
            capture_source=f"{capture_source_a}; B:return_value[{seq_index}]",
        )
        status = result.get("status", "NOT_PROVED")
        compared += 1
        if status != "EQUIVALENT":
            failures.append(result.get("detail", f"seq_index={seq_index} not equivalent"))

    if compared == 0:
        return {
            "idx": idx,
            "case": case_label,
            "status": "NOT_PROVED",
            "detail": f"not proved: B: no comparable circuit captured; fn={fn_b}",
            "capture_source": f"{capture_source_a}; B:",
        }

    if failures:
        return {
            "idx": idx,
            "case": case_label or "",
            "status": "NOT_PROVED",
            "detail": " | ".join(failures),
            "capture_source": f"{capture_source_a}; B:return_value[0..{compared - 1}]",
        }

    return {
        "idx": idx,
        "case": case_label or "",
        "status": "EQUIVALENT",
        "detail": f"fn_a={fn_a}, fn_b={fn_b}, extractor={extractor}, compared={compared}",
        "capture_source": f"{capture_source_a}; B:return_value[0..{compared - 1}]",
    }


def capture_input_circuit_from_candidates(
    candidates: list[tuple[Any, ...]],
    arg_index: int,
) -> tuple[tuple[str, Any] | None, str]:
    if arg_index < 0:
        return None, f"invalid compare_to_input index: {arg_index}"
    last_err = "no candidates tried"
    for candidate in candidates or [tuple()]:
        if arg_index >= len(candidate):
            last_err = f"candidate has only {len(candidate)} argument(s)"
            continue
        extracted = coerce_circuit_like(candidate[arg_index])
        if extracted is not None:
            return extracted, ""
        last_err = f"argument {arg_index} is not a comparable circuit object"
    return None, last_err


def coerce_circuit_like(value: Any) -> tuple[str, Any] | None:
    if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str):
        return value
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit import Gate, Instruction
        if isinstance(value, QuantumCircuit):
            return ("qiskit", value)
        if isinstance(value, (Gate, Instruction)):
            qc = QuantumCircuit(value.num_qubits, getattr(value, "num_clbits", 0))
            qc.append(value, list(range(value.num_qubits)), list(range(getattr(value, "num_clbits", 0))))
            return ("qiskit", qc)
    except Exception:
        pass
    try:
        import cirq
        if isinstance(value, cirq.Circuit):
            return ("cirq", value)
    except Exception:
        pass
    try:
        from pyqpanda3.core import QCircuit, QProg
        if isinstance(value, (QProg, QCircuit)):
            return ("qpanda3", value)
    except Exception:
        pass
    try:
        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
        if isinstance(value, qml.tape.QuantumScript):
            return ("pennylane", value)
        if isinstance(value, qml.QNode):
            args: list[Any] = []
            kwargs: dict[str, Any] = {}
            next_value = 0
            signature = inspect.signature(getattr(value, "func", value))
            defaults = (0.125, 0.25, 0.5, 0.75)
            for parameter in signature.parameters.values():
                if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                    continue
                if parameter.default is not inspect._empty:
                    continue
                assigned = defaults[next_value % len(defaults)]
                next_value += 1
                if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
                    args.append(assigned)
                else:
                    kwargs[parameter.name] = assigned
            script = qml.workflow.construct_tape(value)(*tuple(args), **kwargs)
            return ("pennylane", script)
    except Exception:
        pass
    return None


def call_and_extract_all_circuits(
    t3: Any,
    file_path: Path,
    fn_name: str,
    candidates: list[tuple[Any, ...]],
    extractor: str,
    side: str = "",
    case_label: str | None = None,
) -> tuple[list[tuple[str, Any]], str]:
    mod_name = f"_zx_call_all_{file_path.stem}_{abs(hash((str(file_path), fn_name)))}"
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    try:
        mod = t3._load_module(str(file_path), mod_name)
    except Exception as exc:
        return [], f"load error: {exc}"
    fn = getattr(mod, fn_name, None)
    if fn is None:
        return [], f"function `{fn_name}` not found"

    last_err = "no candidates tried"
    for candidate in candidates or [tuple()]:
        try:
            args = clone_candidate(candidate)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                result = fn(*args)
            circuits = extract_all_circuits_from_result(t3, result, extractor)
            if circuits:
                return circuits, ""
            last_err = f"returned {type(result).__name__}, no circuit extracted"
        except Exception as exc:
            last_err = str(exc)
    suffix = f"; case={case_label}" if case_label else ""
    return [], f"{side}: no comparable circuit captured; fn={fn_name}{suffix}; last={last_err}"


def capture_operator_from_circuit_input(
    t3: Any,
    file_path: Path,
    fn_name: str | None,
    candidates: list[tuple[Any, ...]],
) -> tuple[Any | None, str]:
    if not fn_name:
        return None, "entry function not found"

    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit import Instruction
        from qiskit.quantum_info import Operator
    except Exception as exc:
        return None, f"qiskit import error: {exc}"

    captured: list[Any] = []
    raw_from_circuit = Operator.__dict__.get("from_circuit")
    bound_from_circuit = Operator.from_circuit
    raw_init = Operator.__dict__.get("__init__")

    def remember_circuit(value: Any) -> None:
        if isinstance(value, QuantumCircuit):
            captured.append(value)
        elif isinstance(value, Instruction):
            qc = QuantumCircuit(value.num_qubits, getattr(value, "num_clbits", 0))
            qc.append(value, list(range(value.num_qubits)), list(range(getattr(value, "num_clbits", 0))))
            captured.append(qc)

    def hooked_from_circuit(cls, circuit, *args, **kwargs):
        remember_circuit(circuit)
        return bound_from_circuit(circuit, *args, **kwargs)

    def hooked_init(self, data=None, *args, **kwargs):
        remember_circuit(data)
        return raw_init(self, data, *args, **kwargs)

    Operator.from_circuit = classmethod(hooked_from_circuit)
    Operator.__init__ = hooked_init
    try:
        mod_name = f"_zx_operator_{file_path.stem}_{abs(hash((str(file_path), fn_name)))}"
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        mod = t3._load_module(str(file_path), mod_name)
        fn = getattr(mod, fn_name, None)
        if fn is None:
            return None, f"function `{fn_name}` not found"

        last_err = "no candidates tried"
        for candidate in candidates:
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    fn(*clone_candidate(candidate))
                if captured:
                    return captured[0], ""
                last_err = "Operator.from_circuit was not called with a QuantumCircuit"
            except Exception as exc:
                if captured:
                    return captured[0], ""
                last_err = str(exc)
        return None, last_err
    finally:
        if raw_from_circuit is None:
            try:
                delattr(Operator, "from_circuit")
            except Exception:
                pass
        else:
            Operator.from_circuit = raw_from_circuit
        if raw_init is None:
            try:
                delattr(Operator, "__init__")
            except Exception:
                pass
        else:
            Operator.__init__ = raw_init


def run_state_constructor_capture(
    ctx: RunContext,
    modules: LegacyModules,
    idx: int,
    file_a: Path,
    file_b: Path,
    override: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    t3 = modules.get("type3")
    fn_a = override.get("entry_fn_a") or infer_first_function(file_a)
    fn_b = override.get("entry_fn_b") or infer_matching_function(file_b, fn_a)
    audit["entry_fn"] = fn_a
    case_label = override.get("case_label", "")
    args_a, args_b = build_case_arg_candidates(file_a, file_b, idx, fn_a, fn_b, override)
    if not args_a:
        args_a = [tuple()]
    if not args_b:
        args_b = list(args_a)

    circ_a, err_a = capture_state_constructor_input(t3, file_a, fn_a, args_a)
    if circ_a is None:
        return {"idx": idx, "case": case_label, "status": "NOT_PROVED", "detail": f"not proved: {err_a}", "capture_source": ""}
    circ_b, err_b = capture_state_constructor_input(t3, file_b, fn_b, args_b)
    if circ_b is None:
        return {"idx": idx, "case": case_label, "status": "NOT_PROVED", "detail": f"not proved: {err_b}", "capture_source": "A:state_constructor; B:"}
    return compare_captured_circuits(
        t3,
        idx,
        circ_a,
        circ_b,
        f"fn_a={fn_a}, fn_b={fn_b}, extractor=capture_state_constructor_input",
        case_label=case_label,
        capture_source="A:state_constructor; B:state_constructor",
    )


def capture_state_constructor_input(
    t3: Any,
    file_path: Path,
    fn_name: str,
    candidates: list[tuple[Any, ...]],
) -> tuple[Any | None, str]:
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit import Instruction
        from qiskit.quantum_info import DensityMatrix, StabilizerState, Statevector
    except Exception as exc:
        return None, f"qiskit import error: {exc}"

    captured: list[Any] = []
    originals: list[tuple[type, Any]] = []

    def patch_init(cls):
        original = cls.__init__
        originals.append((cls, original))

        def hooked(self, data=None, *args, **kwargs):
            if isinstance(data, QuantumCircuit):
                captured.append(data)
            elif isinstance(data, Instruction):
                qc = QuantumCircuit(data.num_qubits, getattr(data, "num_clbits", 0))
                qc.append(data, list(range(data.num_qubits)), list(range(getattr(data, "num_clbits", 0))))
                captured.append(qc)
            return original(self, data, *args, **kwargs)

        cls.__init__ = hooked

    for cls in (StabilizerState, Statevector, DensityMatrix):
        patch_init(cls)

    try:
        mod_name = f"_zx_state_{file_path.stem}_{abs(hash((str(file_path), fn_name)))}"
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        mod = t3._load_module(str(file_path), mod_name)
        fn = getattr(mod, fn_name, None)
        if fn is None:
            return None, f"function `{fn_name}` not found"
        last_err = "no candidates tried"
        for candidate in candidates:
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    fn(*clone_candidate(candidate))
                if captured:
                    return captured[0], ""
                last_err = "state constructor ran but no circuit input was captured"
            except Exception as exc:
                if captured:
                    return captured[0], ""
                last_err = str(exc)
        return None, last_err
    finally:
        for cls, original in reversed(originals):
            cls.__init__ = original


def compare_captured_circuits(
    t3: Any,
    idx: int,
    circ_a: Any,
    circ_b: Any,
    detail_prefix: str,
    case_label: str | None = None,
    capture_source: str = "",
) -> dict[str, Any]:
    suffix = f"; case={case_label}" if case_label else ""
    if (
        not (isinstance(circ_a, tuple) and len(circ_a) == 2)
        or not isinstance(circ_a[0], str)
    ):
        circ_a = ("qiskit", circ_a)
    if (
        not (isinstance(circ_b, tuple) and len(circ_b) == 2)
        or not isinstance(circ_b[0], str)
    ):
        circ_b = ("qiskit", circ_b)

    def fallback_result(reason: str) -> dict[str, Any] | None:
        ok, detail = qiskit_operator_fallback_equivalent(circ_a, circ_b)
        if not ok:
            return None
        joined = detail_prefix
        if reason:
            joined += f" | {reason}"
        if detail:
            joined += f" | {detail}"
        joined += suffix
        return {
            "idx": idx,
            "status": "EQUIVALENT",
            "case": case_label or "",
            "detail": joined,
            "capture_source": capture_source,
        }

    try:
        qasm_a = t3.captured_to_qasm(circ_a)
    except Exception as exc:
        detail = str(exc)
        if "MatrixGate" in detail or "Cannot output operation as QASM" in detail:
            detail = f"ZX-QASM path unsupported unitary gate: {detail}"
        fallback = fallback_result(f"fallback_operator after A qasm conversion failed: {detail}")
        if fallback is not None:
            return fallback
        return {
            "idx": idx,
            "case": case_label or "",
            "status": "NOT_PROVED",
            "detail": f"not proved: A qasm conversion failed: {detail}{suffix}",
            "capture_source": capture_source,
        }
    try:
        qasm_b = t3.captured_to_qasm(circ_b)
    except Exception as exc:
        detail = str(exc)
        if "MatrixGate" in detail or "Cannot output operation as QASM" in detail:
            detail = f"ZX-QASM path unsupported unitary gate: {detail}"
        fallback = fallback_result(f"fallback_operator after B qasm conversion failed: {detail}")
        if fallback is not None:
            return fallback
        return {
            "idx": idx,
            "case": case_label or "",
            "status": "NOT_PROVED",
            "detail": f"not proved: B qasm conversion failed: {detail}{suffix}",
            "capture_source": capture_source,
        }
    eq, err = t3.zx_equivalent(qasm_a, qasm_b)
    if eq is None or (err and str(err).startswith(("qasm-parse:", "compare:"))):
        fallback = fallback_result(f"fallback_operator after zx path failed: {err or 'unknown error'}")
        if fallback is not None:
            return fallback
        return {
            "idx": idx,
            "case": case_label or "",
            "status": "NOT_PROVED",
            "detail": f"not proved: {err or 'unknown error'}{suffix}",
            "capture_source": capture_source,
        }
    if not eq:
        fallback = fallback_result(f"fallback_operator after zx reported not equivalent{f': {err}' if err else ''}")
        if fallback is not None:
            return fallback
    return {
        "idx": idx,
        "status": "EQUIVALENT" if eq else "NOT_PROVED",
        "case": case_label or "",
        "detail": detail_prefix + (f" | not proved: {err}" if (err and not eq) else "") + suffix,
        "capture_source": capture_source,
    }


def normalize_qiskit_circuit_for_operator(value: Any) -> Any:
    from qiskit import QuantumCircuit

    if value.parameters:
        bind_map = {parameter: 0.0 for parameter in value.parameters}
        value = value.assign_parameters(bind_map)

    no_meas = value.remove_final_measurements(inplace=False)
    if no_meas is None:
        no_meas = value.copy()
        no_meas.remove_final_measurements(inplace=True)

    cleaned = QuantumCircuit(*no_meas.qregs)
    for instr in no_meas.data:
        operation = instr.operation
        op_name = getattr(operation, "name", "")
        if op_name in ("measure", "reset", "barrier", "delay"):
            continue
        if getattr(operation, "condition", None) is not None:
            continue
        cleaned.append(operation, instr.qubits, instr.clbits)

    try:
        cleaned.global_phase = no_meas.global_phase
    except Exception:
        pass
    return cleaned


def qiskit_operator_fallback_equivalent(
    circ_a: tuple[str, Any],
    circ_b: tuple[str, Any],
) -> tuple[bool, str]:
    if circ_a[0] != "qiskit" or circ_b[0] != "qiskit":
        return False, ""
    try:
        from qiskit.quantum_info import Operator
    except Exception as exc:
        return False, f"fallback_operator unavailable: {exc}"

    try:
        qc_a = normalize_qiskit_circuit_for_operator(circ_a[1])
        qc_b = normalize_qiskit_circuit_for_operator(circ_b[1])
        op_a = Operator(qc_a)
        op_b = Operator(qc_b)
    except Exception as exc:
        return False, f"fallback_operator unavailable: {exc}"

    try:
        equivalent = bool(op_a.equiv(op_b))
    except Exception as exc:
        return False, f"fallback_operator unavailable: {exc}"
    return equivalent, "verified_by=fallback_operator"


def build_arg_candidates_from_manifest(payload: Any, file_path: Path, fn_name: str | None) -> list[tuple[Any, ...]]:
    if not payload:
        return []
    if isinstance(payload, list):
        return [tuple(materialize_value(v) for v in candidate) for candidate in payload]
    if isinstance(payload, dict):
        ordered: list[Any] = []
        names = function_param_names(file_path, fn_name) if fn_name else list(payload)
        for name in names:
            if name in payload:
                ordered.append(materialize_value(payload[name]))
        return [tuple(ordered)]
    return []


def materialize_value(value: Any) -> Any:
    if isinstance(value, dict) and value.get("kind") == "int_key_dict":
        return {int(k): materialize_value(v) for k, v in value.get("items", [])}
    if isinstance(value, dict) and value.get("kind") == "qiskit_dj_oracle":
        return qiskit_dj_oracle(
            variant=str(value.get("variant", "balanced_parity")),
            num_inputs=int(value.get("num_inputs", 3)),
        )
    if isinstance(value, dict) and "kind" in value:
        value = value["kind"]
    if value == "dummy_qiskit_circuit":
        return dummy_qiskit_circuit()
    if value == "dummy_qiskit_circuit_nocbits":
        return dummy_qiskit_circuit(include_clbits=False)
    if value == "dummy_qiskit_circuit_5":
        return dummy_qiskit_circuit(5)
    if value == "dummy_qiskit_parametrized_circuit":
        return dummy_qiskit_parametrized_circuit()
    if value == "dummy_qiskit_parameter_removal_circuit":
        return dummy_qiskit_parameter_removal_circuit()
    if value == "fixed_2q_unitary":
        from qiskit.quantum_info import random_unitary
        return random_unitary(4, seed=42)
    if value == "choi_identity_1q":
        import numpy as np
        return np.eye(4)
    return value


def dummy_qiskit_circuit(n: int = 2, include_clbits: bool = True) -> Any:
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n, n) if include_clbits else QuantumCircuit(n)
    qc.h(0)
    if n > 1:
        qc.cx(0, 1)
    return qc


def qiskit_dj_oracle(variant: str = "balanced_parity", num_inputs: int = 3) -> Any:
    from qiskit import QuantumCircuit

    total_qubits = max(1, int(num_inputs)) + 1
    output = total_qubits - 1
    qc = QuantumCircuit(total_qubits)

    if variant == "constant_zero":
        return qc
    if variant == "constant_one":
        qc.x(output)
        return qc
    if variant == "balanced_parity":
        for qubit in range(output):
            qc.cx(qubit, output)
        return qc

    raise ValueError(f"unknown qiskit_dj_oracle variant: {variant}")


def dummy_qiskit_parametrized_circuit(n: int = 2, include_clbits: bool = True) -> Any:
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter

    theta = Parameter("theta")
    phi = Parameter("phi")
    qc = QuantumCircuit(n, n) if include_clbits else QuantumCircuit(n)
    qc.rx(theta, 0)
    if n > 1:
        qc.cx(0, 1)
        qc.ry(phi, 1)
    return qc


def dummy_qiskit_parameter_removal_circuit() -> Any:
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter

    theta = Parameter("theta")
    phi = Parameter("phi")
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    qc.ry(0.2, 0)
    qc.rz(phi, 0)
    return qc


def function_param_names(file_path: Path, fn_name: str | None) -> list[str]:
    if not fn_name:
        return []
    try:
        src = file_path.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(file_path))
    except Exception:
        return []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == fn_name:
            return [arg.arg for arg in node.args.args]
    return []


def infer_first_function(file_path: Path) -> str | None:
    try:
        src = file_path.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(file_path))
    except Exception:
        return None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            return node.name
    return None


def infer_matching_function(file_path: Path, gt_fn: str | None) -> str | None:
    names: list[str] = []
    try:
        src = file_path.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(file_path))
        names = [
            node.name for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
    except Exception:
        return gt_fn
    if gt_fn:
        for suffix in ("_llm", "_llm_fixed", "_llm_corrected"):
            candidate = f"{gt_fn}{suffix}"
            if candidate in names:
                return candidate
        if gt_fn in names:
            return gt_fn
    for name in names:
        if "_llm" in name or name.endswith("_fixed") or name.endswith("_corrected"):
            return name
    return names[0] if names else gt_fn


def write_reports(ctx: RunContext, rows: list[dict[str, Any]], audit_rows: list[dict[str, Any]]) -> None:
    ctx.out_path.parent.mkdir(parents=True, exist_ok=True)
    ctx.csv_path.parent.mkdir(parents=True, exist_ok=True)
    ctx.audit_path.parent.mkdir(parents=True, exist_ok=True)

    n_eq = sum(1 for row in rows if row["result"] == "EQUIVALENT")
    n_np = len(rows) - n_eq

    with ctx.out_path.open("w", encoding="utf-8", newline="") as f:
        f.write(f"# ZX Equivalence Verification Report - {ctx.source_class}\n\n")
        f.write(f"**Side A:** `{ctx.dir_a}` / `{ctx.pattern_a}`  \n")
        f.write(f"**Side B:** `{ctx.dir_b}` / `{ctx.pattern_b}`  \n")
        f.write("**Routing:** source_class controls this report; internal route details are recorded in routing-audit.jsonl.\n\n")
        f.write(
            f"**Summary:** Equivalent = {n_eq} / {len(rows)}, "
            f"Not Proved = {n_np}.\n\n"
        )
        f.write("| index | case | result | zx_equivalent | capture_source | notes |\n")
        f.write("|:-----:|:-----|:------:|:-------------:|:---------------|:------|\n")
        for row in rows:
            notes = str(row["notes"]).replace("|", "\\|").replace("\n", " ")
            source = str(row.get("capture_source", "")).replace("|", "\\|").replace("\n", " ")
            case = str(row.get("case", "")).replace("|", "\\|").replace("\n", " ")
            if len(notes) > 300:
                notes = notes[:300] + "..."
            f.write(
                f"| {row['index']} | {case} | {STATUS_EN.get(row['result'], row['result'])} | "
                f"{bool(row.get('zx_equivalent'))} | {source} | {notes} |\n"
            )

    with ctx.csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["index", "case", "result", "zx_equivalent", "notes", "capture_source"],
        )
        writer.writeheader()
        writer.writerows(rows)

    with ctx.audit_path.open("w", encoding="utf-8", newline="") as f:
        for row in audit_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit("Run one of the compatibility scripts instead.")
