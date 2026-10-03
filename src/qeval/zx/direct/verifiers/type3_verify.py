"""
third.py

Generic ZX-equivalence verifier for Type 3 quantum programs (circuit-output).
Type 3: the entry function directly RETURNS a QuantumCircuit object.

Strategy:
  1. Parse codes/codeN.py -> find entry function (via `# 入口函数:` comment or AST scan).
  2. Parse llms/llmN.py   -> find matching `{fn}_llm` function (or any `*_llm` top-level fn).
  3. Build argument candidates from signature defaults + __main__ block test values.
  4. Call both functions; extract returned QuantumCircuit (handles tuple returns).
  5. Bind unbound parameters (parametrized circuits) to 0.0.
  6. Strip measurements, decompose to QASM2, compare ZX circuits with `verify_equality`.

CLI (compatible with zx_type1_mostnew.py interface):
  python third.py \\
    --dir-a  <dir_A>  --pattern-a 'code{idx}.py'  --framework-a auto \\
    --dir-b  <dir_B>  --pattern-b 'llm{idx}.py'   --framework-b auto \\
    --indices <all|n,m,p-q> \\
    --out     <report.md> \\
    [--path-add <extra_import_dir>]
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")


class NonUnitaryCirqOperationError(ValueError):
    pass


# ---------------------------------------------------------------------------
# Module loader
# ---------------------------------------------------------------------------
def _load_module(filepath: str, mod_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        spec.loader.exec_module(mod)
    return mod


def detect_framework(filepath: str) -> str:
    try:
        content = Path(filepath).read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return "qiskit"
    has_pennylane = "import pennylane" in content or "from pennylane" in content
    has_cirq = "import cirq" in content or "from cirq" in content
    has_qiskit = "import qiskit" in content or "from qiskit" in content
    if has_pennylane and not has_cirq and not has_qiskit:
        return "pennylane"
    if has_cirq and not has_qiskit:
        return "cirq"
    return "qiskit"


# ---------------------------------------------------------------------------
# Entry function discovery
# ---------------------------------------------------------------------------
def _comment_entry_fn(filepath: Path) -> str | None:
    """Read `# 入口函数: fn_name` header comment."""
    try:
        text = filepath.read_text(encoding="utf-8-sig", errors="replace")
        m = re.search(r"#\s*入口函数\s*:\s*(\w+)", text)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def _top_level_fns(filepath: Path) -> list[str]:
    try:
        src = filepath.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(filepath))
        return [
            n.name for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
    except Exception:
        return []


def find_entry_fn_codes(filepath: Path) -> str | None:
    """Entry function for a codes/codeN.py file."""
    fn = _comment_entry_fn(filepath)
    if fn:
        return fn
    fns = _top_level_fns(filepath)
    # Skip private/helper names
    for name in fns:
        if not name.startswith("_"):
            return name
    return None


def find_llm_fn(filepath: Path, gt_fn: str | None) -> str | None:
    """LLM function in llms/llmN.py.

    Priority: {gt_fn}_llm > {gt_fn}_llm_fixed > any *_llm* suffix
              > *_corrected > *_fixed > any name containing 'llm'.
    """
    fns = _top_level_fns(filepath)
    if gt_fn:
        for suffix in ("_llm", "_llm_fixed", "_llm_corrected"):
            candidate = f"{gt_fn}{suffix}"
            if candidate in fns:
                return candidate
    llm_fns = [n for n in fns if "_llm" in n]
    if llm_fns:
        return llm_fns[0]
    # Fallback: corrected / fixed variants that represent the LLM answer
    for suffix in ("_corrected", "_fixed"):
        alts = [n for n in fns if n.endswith(suffix) and not n.endswith("_gt")]
        if alts:
            return alts[0]
    llm_fns = [n for n in fns if "llm" in n.lower()]
    if llm_fns:
        return llm_fns[0]
    return None


# ---------------------------------------------------------------------------
# Argument inference
# ---------------------------------------------------------------------------
def _dummy_circuit(n: int = 2):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n)
    qc.h(0)
    if n > 1:
        qc.cx(0, 1)
    return qc


def _dummy_parametrized_circuit():
    from qiskit.circuit import QuantumCircuit, Parameter
    theta = Parameter("theta")
    phi = Parameter("phi")
    qc = QuantumCircuit(2)
    qc.rx(theta, 0)
    qc.ry(phi, 1)
    return qc


# Sensible defaults keyed by parameter name (lowercase)
_NAME_DEFAULTS: dict[str, object] = {
    "n_qubits": 3,   "num_qubits": 3,  "nqubits": 3,
    # 'n' intentionally omitted — handled with multi-value candidates
    "k": 3,          "qubits": 3,      "num_ancilla": 1,
    "theta": 0.5,    "phi": 0.5,       "lam": 0.5,
    "gamma": 0.5,    "angle": 0.5,     "value": None,
    "drawing": False, "measure": False,
    "with_measurements": False, "insert_barriers": False,
    "barriers": False,
    "position": 0,   "index": 0,       "qubit": 0,
    "target": 1,     "control": 0,     "pos": 0,
    "s": "101",      "bitstring": "101", "secret": "101", "hidden": "101",
    "reps": 2,       "repetitions": 1,  "order": 1,
    "seed": 42,      "shots": 1024,
    # Hamiltonian simulation
    "pauli_strings": ["ZI", "IZ"],
    "times": [0.5, 0.5],
    "pauli_string": "XYZ",
    "time": 0.5,
    # quantum teleportation data (list of gate instructions)
    "data": [],
    # probability distribution
    "probability_dist": {0: 0.5, 1: 0.5},
}


def _infer_param_default(param_name: str) -> object:
    low = param_name.lower()
    if low in _NAME_DEFAULTS:
        return _NAME_DEFAULTS[low]
    if "qubit" in low or "n_q" in low:
        return 3
    if "angle" in low or "theta" in low or "phi" in low:
        return 0.5
    if "draw" in low or "measure" in low or "bool" in low:
        return False
    if low in ("circuit", "qc", "circ", "quantum_circuit"):
        return _dummy_circuit()
    if "circuit" in low or "qc_" in low:
        return _dummy_circuit()
    if "string" in low or "secret" in low or "bitstr" in low:
        return "101"
    if "position" in low or "index" in low or "idx" == low:
        return 0
    if "rep" in low:
        return 1
    return None


def _extract_main_call_args(filepath: Path, fn_name: str) -> tuple | None:
    """Extract positional args from the __main__ block call to fn_name."""
    try:
        src = filepath.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(filepath))
    except Exception:
        return None
    for node in tree.body:
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not (isinstance(test, ast.Compare) and
                isinstance(test.left, ast.Name) and test.left.id == "__name__"):
            continue
        for stmt in ast.walk(node):
            if not isinstance(stmt, ast.Call):
                continue
            func = stmt.func
            called = (func.id if isinstance(func, ast.Name) else
                      func.attr if isinstance(func, ast.Attribute) else None)
            if called != fn_name:
                continue
            args = []
            for a in stmt.args:
                try:
                    args.append(ast.literal_eval(a))
                except Exception:
                    args.append(None)
            return tuple(args)
    return None


def build_arg_candidates(filepath: Path, fn_name: str) -> list[tuple]:
    """Return a prioritized list of positional-arg tuples to try."""
    try:
        src = filepath.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(filepath))
    except Exception:
        return [()]

    fn_def = next(
        (n for n in tree.body
         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == fn_name),
        None,
    )
    if fn_def is None:
        return [()]

    params = fn_def.args.args or []
    defaults = fn_def.args.defaults or []
    n_params = len(params)
    n_defaults = len(defaults)
    offset = n_params - n_defaults

    param_vals: list[object] = []
    for i, param in enumerate(params):
        di = i - offset
        if di >= 0:
            try:
                param_vals.append(ast.literal_eval(defaults[di]))
            except Exception:
                param_vals.append(_infer_param_default(param.arg))
        else:
            param_vals.append(_infer_param_default(param.arg))

    candidates: list[tuple] = []
    if param_vals:
        candidates.append(tuple(param_vals))
    candidates.append(())

    # For "n"-named integer params (circuit size), also try larger values
    # (some functions access qubit indices up to n-1 and need n>=5)
    _n_like = {"n", "num", "size", "width"}
    has_n_param = any(p.arg.lower() in _n_like for p in params)
    if has_n_param:
        for n_val in (5, 4, 2):
            alt = list(param_vals)
            changed = False
            for j, p in enumerate(params):
                if p.arg.lower() in _n_like:
                    alt[j] = n_val
                    changed = True
            if changed:
                t = tuple(alt)
                if t not in candidates:
                    candidates.append(t)

    # For "circuit/qc" params, also try a parametrized circuit (for param-stripping fns)
    _circ_like = {"circuit", "qc", "circ", "quantum_circuit"}
    if any(p.arg.lower() in _circ_like for p in params):
        alt = list(param_vals)
        changed = False
        for j, p in enumerate(params):
            if p.arg.lower() in _circ_like:
                alt[j] = _dummy_parametrized_circuit()
                changed = True
        if changed:
            t = tuple(alt)
            if t not in candidates:
                candidates.append(t)
        # Also try a 5-qubit circuit (for mcy-style functions)
        alt5 = list(param_vals)
        changed5 = False
        for j, p in enumerate(params):
            if p.arg.lower() in _circ_like:
                alt5[j] = _dummy_circuit(5)
                changed5 = True
        if changed5:
            t5 = tuple(alt5)
            if t5 not in candidates:
                candidates.append(t5)

    main_args = _extract_main_call_args(filepath, fn_name)
    if main_args and main_args not in candidates:
        candidates.insert(1, main_args)

    return candidates


# ---------------------------------------------------------------------------
# Circuit capture
# ---------------------------------------------------------------------------
def _extract_qiskit_circuit(result) -> tuple[str, object] | None:
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit import Gate, Instruction
        if isinstance(result, QuantumCircuit):
            return ("qiskit", result)
        if isinstance(result, (Gate, Instruction)):
            defn = getattr(result, "definition", None)
            if isinstance(defn, QuantumCircuit):
                return ("qiskit", defn)
            try:
                nq = result.num_qubits
                qc = QuantumCircuit(nq)
                qc.append(result, range(nq))
                return ("qiskit", qc)
            except Exception:
                pass
    except Exception:
        pass
    return None


def _extract_cirq_circuit(result) -> tuple[str, object] | None:
    try:
        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import cirq
        if isinstance(result, cirq.Circuit):
            return ("cirq", result)
    except Exception:
        pass
    return None


def _extract_qpanda3_circuit(result) -> tuple[str, object] | None:
    try:
        from pyqpanda3.core import QProg, QCircuit
        if isinstance(result, (QProg, QCircuit)):
            return ("qpanda3", result)
    except Exception:
        pass
    return None


_PENNYLANE_PARAM_VALUES = (0.125, 0.25, 0.5, 0.75)


def _import_pennylane():
    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        import pennylane as qml
    return qml


def _pennylane_call_args(value) -> tuple[tuple[object, ...], dict[str, object]]:
    args: list[object] = []
    kwargs: dict[str, object] = {}
    next_value = 0
    signature = inspect.signature(value)
    for parameter in signature.parameters.values():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter.default is not inspect._empty:
            continue
        assigned = _PENNYLANE_PARAM_VALUES[next_value % len(_PENNYLANE_PARAM_VALUES)]
        next_value += 1
        if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            args.append(assigned)
        else:
            kwargs[parameter.name] = assigned
    return tuple(args), kwargs


def _pennylane_qnode_to_script(value):
    qml = _import_pennylane()
    args, kwargs = _pennylane_call_args(getattr(value, "func", value))
    return qml.workflow.construct_tape(value)(*args, **kwargs)


def _pennylane_callable_to_script(value):
    qml = _import_pennylane()
    args, kwargs = _pennylane_call_args(value)
    return qml.tape.make_qscript(value)(*args, **kwargs)


def _extract_pennylane_circuit(result) -> tuple[str, object] | None:
    try:
        qml = _import_pennylane()
        if isinstance(result, qml.QNode):
            return ("pennylane", _pennylane_qnode_to_script(result))
        if isinstance(result, qml.tape.QuantumScript):
            return ("pennylane", result)
        if callable(result):
            qml_module = getattr(result, "__globals__", {}).get("qml")
            if getattr(qml_module, "__name__", "") == "pennylane":
                return ("pennylane", _pennylane_callable_to_script(result))
    except Exception:
        pass
    return None


def extract_returned_circuit(result) -> tuple[str, object] | None:
    """Pull the first comparable circuit object out of a return value."""
    for extractor in (
        _extract_qiskit_circuit,
        _extract_pennylane_circuit,
        _extract_cirq_circuit,
        _extract_qpanda3_circuit,
    ):
        captured = extractor(result)
        if captured is not None:
            return captured

    if isinstance(result, (tuple, list)):
        for item in result:
            captured = extract_returned_circuit(item)
            if captured is not None:
                return captured

    if isinstance(result, dict):
        for item in result.values():
            captured = extract_returned_circuit(item)
            if captured is not None:
                return captured

    return None


def capture_circuit(filepath: str, fn_name: str, arg_candidates: list[tuple]) -> tuple[tuple[str, object] | None, str]:
    """Load module, call fn_name with candidate args, return ((framework, circuit), error_msg)."""
    # Use a unique module name to avoid cross-contamination in sys.modules
    mod_name = f"_t3_{Path(filepath).stem}_{abs(hash(filepath))}"
    # Always reload so parallel pairs don't share state
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    try:
        mod = _load_module(filepath, mod_name)
    except Exception as e:
        return None, f"load error: {e}"

    fn = getattr(mod, fn_name, None)
    if fn is None:
        return None, f"function `{fn_name}` not found in module"

    last_err = "no candidates tried"
    for args in arg_candidates:
        try:
            devnull = io.StringIO()
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                result = fn(*args)
            circ = extract_returned_circuit(result)
            if circ is not None:
                return circ, ""
            last_err = f"returned {type(result).__name__}, no comparable circuit extracted"
        except Exception as e:
            last_err = str(e)

    return None, f"all {len(arg_candidates)} arg candidate(s) failed; last: {last_err}"


# ---------------------------------------------------------------------------
# QASM export + ZX comparison
# ---------------------------------------------------------------------------
PYZX_BASIS = [
    "cx", "cz", "h", "x", "y", "z", "s", "sdg", "t", "tdg",
    "rx", "ry", "rz", "u1", "u2", "u3", "p", "ccx", "swap",
]


def qiskit_to_qasm(qcirc) -> str:
    from qiskit import QuantumCircuit, qasm2, transpile

    # Bind unbound parameters (parametrized circuits) to 0.0
    if qcirc.parameters:
        bind_map = {p: 0.0 for p in qcirc.parameters}
        qcirc = qcirc.assign_parameters(bind_map)

    try:
        qcirc = _lower_qiskit_circuit_for_qasm(qcirc)
    except Exception:
        pass

    no_meas = qcirc.remove_final_measurements(inplace=False)
    if no_meas is None:
        no_meas = qcirc.copy()
        no_meas.remove_final_measurements(inplace=True)

    cleaned = QuantumCircuit(*no_meas.qregs)
    for instr in no_meas.data:
        op_name = instr.operation.name
        if op_name in ("measure", "reset", "barrier", "delay"):
            continue
        if getattr(instr.operation, "condition", None) is not None:
            continue
        cleaned.append(instr.operation, instr.qubits, instr.clbits)

    decomposed = transpile(cleaned, basis_gates=PYZX_BASIS, optimization_level=0)
    return qasm2.dumps(decomposed)


def _lower_qiskit_circuit_for_qasm(qcirc):
    from qiskit import QuantumCircuit

    lowered = QuantumCircuit(*qcirc.qregs, *qcirc.cregs, name=qcirc.name)
    try:
        lowered.global_phase = qcirc.global_phase
    except Exception:
        pass

    for instr in qcirc.data:
        operation = instr.operation
        qubits = instr.qubits
        clbits = instr.clbits

        lowered_op = _lower_qiskit_operation(operation)
        if lowered_op is None:
            lowered.append(operation, qubits, clbits)
            continue

        if isinstance(lowered_op, QuantumCircuit):
            lowered.compose(lowered_op, qubits=qubits, clbits=clbits, inplace=True)
        else:
            lowered.append(lowered_op, qubits, clbits)
    return lowered


def _lower_qiskit_operation(operation):
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit.library import PauliEvolutionGate
        from qiskit.quantum_info import SparsePauliOp
    except Exception:
        return None

    if isinstance(operation, PauliEvolutionGate):
        operator = getattr(operation, "operator", None)
        time = getattr(operation, "time", None)
        if operator is None or time is None:
            return None
        if not isinstance(operator, SparsePauliOp):
            try:
                operator = SparsePauliOp(operator)
            except Exception:
                return None

        # Build a concrete circuit from the Pauli terms instead of relying on
        # Qiskit's abstract synthesis objects during QASM export.
        lowered = QuantumCircuit(operation.num_qubits)
        try:
            terms = operator.to_list()
        except Exception:
            return None

        for label, coeff in terms:
            term = _pauli_term_evolution_circuit(label, complex(coeff) * float(time))
            if term is None:
                return None
            lowered.compose(term, inplace=True)
        return lowered
    return None


def _pauli_term_evolution_circuit(label: str, theta: complex):
    from math import pi
    from qiskit import QuantumCircuit

    if abs(theta.imag) > 1e-9:
        return None
    angle = float(theta.real)
    active = [idx for idx, char in enumerate(label) if char != "I"]
    circuit = QuantumCircuit(len(label))
    if not active:
        return circuit

    pivot = active[-1]
    for idx in active:
        pauli = label[idx]
        if pauli == "X":
            circuit.h(idx)
        elif pauli == "Y":
            circuit.sdg(idx)
            circuit.h(idx)
        elif pauli == "Z":
            pass
        else:
            return None

    for idx in active[:-1]:
        circuit.cx(idx, pivot)
    circuit.rz(2 * angle, pivot)
    for idx in reversed(active[:-1]):
        circuit.cx(idx, pivot)

    for idx in active:
        pauli = label[idx]
        if pauli == "X":
            circuit.h(idx)
        elif pauli == "Y":
            circuit.h(idx)
            circuit.s(idx)
        elif pauli == "Z":
            pass
        else:
            return None
    return circuit


def cirq_to_qasm(ccirc) -> str:
    import cirq

    all_qubits = sorted(ccirc.all_qubits())

    def _is_measurement(op) -> bool:
        return hasattr(cirq, "is_measurement") and cirq.is_measurement(op)

    def _is_reset(op) -> bool:
        gate = getattr(op, "gate", None)
        return gate is not None and isinstance(gate, getattr(cirq, "ResetChannel", ()))

    def _is_state_preparation(op) -> bool:
        gate = getattr(op, "gate", None)
        return gate is not None and isinstance(gate, getattr(cirq, "StatePreparationChannel", ()))

    def _is_non_unitary_noise(op) -> bool:
        if _is_measurement(op) or _is_reset(op) or _is_state_preparation(op):
            return False
        try:
            return not cirq.has_unitary(op)
        except Exception:
            return False

    ops = []
    for op in ccirc.all_operations():
        if _is_measurement(op):
            continue
        if _is_reset(op):
            raise NonUnitaryCirqOperationError("cirq reset operation is not comparable via ZX")
        if _is_non_unitary_noise(op):
            raise NonUnitaryCirqOperationError("cirq non-unitary noise operation is not comparable via ZX")
        if isinstance(op, cirq.TaggedOperation):
            op = op.untagged
        ops.append(op)

    expanded = []
    for op in ops:
        try:
            cirq.qasm(cirq.Circuit(op))
            expanded.append(op)
        except Exception:
            try:
                decomposed = cirq.decompose(
                    op,
                    keep=lambda o: cirq.num_qubits(o) <= 2 and cirq.has_unitary(o),
                    on_stuck_raise=None,
                )
                expanded.extend(decomposed)
            except Exception:
                try:
                    u = cirq.unitary(op)
                    qs = list(op.qubits)
                    expanded.append(cirq.MatrixGate(u).on(*qs))
                except Exception:
                    pass

    no_meas = cirq.Circuit(expanded)
    used = set(no_meas.all_qubits())
    for q in all_qubits:
        if q not in used:
            no_meas.append(cirq.I(q))

    try:
        return cirq.qasm(no_meas)
    except Exception:
        decomposed = cirq.optimize_for_target_gateset(
            no_meas, gateset=cirq.CZTargetGateset()
        )
        return cirq.qasm(decomposed)


def qpanda3_to_qasm(prog) -> str:
    from pyqpanda3.intermediate_compiler import convert_qprog_to_qasm
    from pyqpanda3.core import QProg, QCircuit

    if isinstance(prog, QCircuit):
        p = QProg()
        p << prog
        prog = p

    try:
        qasm_raw = convert_qprog_to_qasm(prog)
    except Exception as e:
        raise RuntimeError(f"QPanda3 -> QASM failed: {e}") from e

    lines = qasm_raw.splitlines()
    filtered = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("measure"):
            continue
        if stripped.startswith("creg"):
            continue
        filtered.append(line)

    return "\n".join(filtered)


def pennylane_to_qasm(circuit) -> str:
    qml = _import_pennylane()
    if isinstance(circuit, qml.QNode):
        circuit = _pennylane_qnode_to_script(circuit)
    elif callable(circuit) and not isinstance(circuit, qml.tape.QuantumScript):
        qml_module = getattr(circuit, "__globals__", {}).get("qml")
        if getattr(qml_module, "__name__", "") == "pennylane":
            circuit = _pennylane_callable_to_script(circuit)
    qasm_raw = qml.to_openqasm(circuit)
    if callable(qasm_raw):
        qasm_raw = qasm_raw()
    filtered = []
    for line in str(qasm_raw).splitlines():
        stripped = line.strip()
        if stripped.startswith("measure") or stripped.startswith("creg"):
            continue
        filtered.append(line)
    return "\n".join(filtered)


def captured_to_qasm(captured: tuple[str, object]) -> str:
    framework, circ = captured
    if framework == "qiskit":
        return qiskit_to_qasm(circ)
    if framework == "cirq":
        return cirq_to_qasm(circ)
    if framework == "qpanda3":
        return qpanda3_to_qasm(circ)
    if framework == "pennylane":
        return pennylane_to_qasm(circ)
    raise ValueError(f"unknown framework: {framework}")


def zx_equivalent(qasm_a: str, qasm_b: str) -> tuple[bool, str]:
    import pyzx as zx
    try:
        ca = zx.Circuit.from_qasm(qasm_a)
        cb = zx.Circuit.from_qasm(qasm_b)
    except Exception as e:
        return False, f"qasm-parse: {e}"
    if ca.qubits != cb.qubits:
        return False, f"qubit mismatch {ca.qubits} vs {cb.qubits}"
    try:
        eq = ca.verify_equality(cb, up_to_global_phase=True)
        return bool(eq), ""
    except Exception as e:
        return False, f"verify_equality failed: {e}"


# ---------------------------------------------------------------------------
# Per-pair runner
# ---------------------------------------------------------------------------
def run_pair_type3(
    idx: int,
    file_a: str,
    file_b: str,
    framework_a: str | None = None,
    framework_b: str | None = None,
) -> dict:
    out: dict = {"idx": idx, "status": "PENDING", "detail": ""}
    pa, pb = Path(file_a), Path(file_b)

    # ---- find functions ----
    fn_a = find_entry_fn_codes(pa)
    if fn_a is None:
        out["status"] = "UNSUPPORTED"
        out["detail"] = "A: 未找到入口函数"
        return out

    fn_b = find_llm_fn(pb, fn_a)
    if fn_b is None:
        # Fall back to same name
        fn_b = fn_a

    # ---- build arg candidates ----
    args_a = build_arg_candidates(pa, fn_a)
    args_b = build_arg_candidates(pb, fn_b)
    # Cross-pollinate: A's candidates are also valid for B (same task, same signature)
    for cand in args_a:
        if cand not in args_b:
            args_b.append(cand)

    # ---- capture circuits ----
    captured_a, err_a = capture_circuit(file_a, fn_a, args_a)
    if captured_a is None:
        out["status"] = "CAPTURE_FAIL"
        out["detail"] = f"A [{fn_a}]: {err_a}"
        return out

    captured_b, err_b = capture_circuit(file_b, fn_b, args_b)
    if captured_b is None:
        out["status"] = "CAPTURE_FAIL"
        out["detail"] = f"B [{fn_b}]: {err_b}"
        return out

    # ---- QASM export ----
    try:
        qasm_a = captured_to_qasm(captured_a)
    except Exception as e:
        out["status"] = "ERROR"
        out["detail"] = f"A QASM [{fn_a}]: {e}"
        return out
    try:
        qasm_b = captured_to_qasm(captured_b)
    except Exception as e:
        out["status"] = "ERROR"
        out["detail"] = f"B QASM [{fn_b}]: {e}"
        return out

    # ---- ZX comparison ----
    eq, err = zx_equivalent(qasm_a, qasm_b)
    out["status"] = "EQUIVALENT" if eq else "NOT_PROVED"
    out["detail"] = f"fn_a={fn_a}, fn_b={fn_b}" + (f" | {err}" if err else "")
    return out


# ---------------------------------------------------------------------------
# Index / path helpers
# ---------------------------------------------------------------------------
def _parse_indices(spec: str) -> list[int]:
    if not spec or spec.lower() in ("all", "*"):
        return []
    parsed: list[int] = []
    for raw in spec.split(","):
        token = raw.strip()
        if not token:
            continue
        if "-" in token:
            a, b = token.split("-", 1)
            start, end = int(a.strip()), int(b.strip())
            step = 1 if end >= start else -1
            parsed.extend(range(start, end + step, step))
        else:
            parsed.append(int(token))
    seen: set[int] = set()
    unique: list[int] = []
    for idx in parsed:
        if idx not in seen:
            seen.add(idx)
            unique.append(idx)
    return unique


def _compile_idx_pattern(pattern: str) -> re.Pattern:
    if "{idx}" not in pattern:
        raise ValueError("pattern must contain '{idx}' placeholder")
    regex = "^" + re.escape(pattern).replace(r"\{idx\}", r"(?P<idx>\d+)") + "$"
    return re.compile(regex)


def _discover_indices(directory: Path, pattern: str) -> set[int]:
    rx = _compile_idx_pattern(pattern)
    found: set[int] = set()
    for entry in directory.iterdir():
        if entry.is_file():
            m = rx.match(entry.name)
            if m:
                found.add(int(m.group("idx")))
    return found


def _resolve_path(base: Path, path_like: str) -> Path:
    p = Path(path_like)
    return p if p.is_absolute() else base / p


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None):
    from zx_unified import legacy_main
    return legacy_main("type3", globals(), argv)

    parser = argparse.ArgumentParser(
        description="ZX verifier for Type 3 (circuit-output) quantum program pairs."
    )
    parser.add_argument("--dir-a",     default="class3/codes",
                        help="Side A directory (ground truth).")
    parser.add_argument("--dir-b",     default="class3/llms",
                        help="Side B directory (LLM generated).")
    parser.add_argument("--pattern-a", default="code{idx}.py",
                        help="Filename template for side A (must contain {idx}).")
    parser.add_argument("--pattern-b", default="llm{idx}.py",
                        help="Filename template for side B (must contain {idx}).")
    parser.add_argument("--framework-a", choices=["auto", "qiskit", "cirq"], default="auto")
    parser.add_argument("--framework-b", choices=["auto", "qiskit", "cirq"], default="auto")
    parser.add_argument("--indices",   default="all",
                        help="Comma-separated indices or ranges (e.g. 0,3,5-10) or 'all'.")
    parser.add_argument("--out",       default="resulttype3.md",
                        help="Output markdown report path.")
    parser.add_argument("--path-add",  action="append", default=[],
                        help="Extra sys.path entry (repeatable).")
    args = parser.parse_args(argv)

    base   = Path(__file__).resolve().parent
    dir_a  = _resolve_path(base, args.dir_a)
    dir_b  = _resolve_path(base, args.dir_b)
    out_p  = _resolve_path(base, args.out)
    extras = [_resolve_path(base, p) for p in args.path_add]

    if not dir_a.is_dir():
        parser.error(f"--dir-a is not a directory: {dir_a}")
    if not dir_b.is_dir():
        parser.error(f"--dir-b is not a directory: {dir_b}")

    for p in [base, dir_a.parent, dir_b.parent, dir_a, dir_b, *extras]:
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)

    if not args.indices or args.indices.lower() in ("all", "*"):
        idx_a = _discover_indices(dir_a, args.pattern_a)
        idx_b = _discover_indices(dir_b, args.pattern_b)
        indices = sorted(idx_a & idx_b)
        if not indices:
            parser.error("no paired files found matching pattern-a and pattern-b")
    else:
        indices = _parse_indices(args.indices)

    fw_a = None if args.framework_a == "auto" else args.framework_a
    fw_b = None if args.framework_b == "auto" else args.framework_b

    results: list[dict] = []
    for idx in indices:
        file_a = dir_a / args.pattern_a.format(idx=idx)
        file_b = dir_b / args.pattern_b.format(idx=idx)

        if not file_a.exists() or not file_b.exists():
            missing = []
            if not file_a.exists():
                missing.append(f"A:{file_a}")
            if not file_b.exists():
                missing.append(f"B:{file_b}")
            r = {"idx": idx, "status": "MISSING", "detail": "; ".join(missing)}
        else:
            r = run_pair_type3(idx, str(file_a), str(file_b), fw_a, fw_b)

        results.append(r)
        print(f"[{idx:>3}]  {r['status']:<14}  {r['detail'][:200]}")

    n_eq  = sum(1 for r in results if r["status"] == "EQUIVALENT")
    n_ne  = sum(1 for r in results if r["status"] == "NOT_PROVED")
    n_err = sum(1 for r in results if r["status"] not in ("EQUIVALENT", "NOT_PROVED"))

    with open(out_p, "w", encoding="utf-8") as f:
        f.write("# ZX 等价性验证 — 第三类量子程序（输出为量子电路图）\n\n")
        f.write(f"- 侧 A（标准答案）：`{args.dir_a}` / `{args.pattern_a}`\n")
        f.write(f"- 侧 B（大模型答案）：`{args.dir_b}` / `{args.pattern_b}`\n\n")
        f.write(
            "**方法：** 直接调用入口函数捕获返回的 `QuantumCircuit` 对象；"
            "绑定参数化电路的未绑定参数（统一置 0.0）；"
            "去除测量/reset/barrier；转换为 OpenQASM 2.0；"
            "使用 `Circuit.verify_equality(..., up_to_global_phase=True)` 比较 ZX 等价性。\n\n"
        )
        f.write(
            f"**汇总：** EQUIVALENT（等价）= **{n_eq}** / {len(results)}，"
            f"NOT_PROVED（未证得等价）= {n_ne}，"
            f"ERROR/FAIL（错误/失败）= {n_err}。\n\n"
        )
        f.write("| 序号 | ZX 等价性结果 | 备注 |\n")
        f.write("|:----:|:------------:|:----|\n")
        for r in results:
            d = r["detail"].replace("|", "\\|").replace("\n", " ")
            if len(d) > 240:
                d = d[:240] + "…"
            f.write(f"| {r['idx']} | {r['status']} | {d} |\n")

    print(f"\n报告已写入：{out_p}")
    print(f"汇总：EQUIVALENT={n_eq}, NOT_PROVED={n_ne}, ERROR/FAIL={n_err}, 共 {len(results)} 对")


if __name__ == "__main__":
    main()
