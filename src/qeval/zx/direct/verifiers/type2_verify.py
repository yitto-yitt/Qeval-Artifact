"""
type2-three.py

ZX equivalence verifier for Type B quantum programs (statevector / quantum-state output).
Supports 6 framework combinations:
  qiskit-qiskit, cirq-cirq, qiskit-cirq,
  Qpanda3-Qpanda3, cirq-Qpanda3, qiskit-Qpanda3

Strategy (intercept statevector simulation + strip measurements):
  1. Qiskit: monkey-patch Statevector.from_instruction / DensityMatrix.from_instruction
     to capture quantum circuit objects. Programs using only analytical APIs
     (random_density_matrix, random_statevector, etc.) are tagged NOT_APPLICABLE.
  2. Cirq: monkey-patch Simulator.simulate / run to capture circuits.
  3. QPanda3: monkey-patch CPUQVM.run to capture QProg objects.
  4. Strip non-unitary operations, convert to OpenQASM 2.0, build pyzx circuit -> ZX graph.
  5. Compare via `Circuit.verify_equality(..., up_to_global_phase=True)`.

CLI:
  python type2-three.py \\
    --dir-a <dirA> --pattern-a '<templateA with {idx}>' --framework-a <auto|qiskit|cirq|Qpanda3> \\
    --dir-b <dirB> --pattern-b '<templateB with {idx}>' --framework-b <auto|qiskit|cirq|Qpanda3> \\
    --indices <all or index list> \\
    --out <report.md>
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib.util
import io
import math
import re
import sys
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")

try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    matplotlib = None


# ---------------------------------------------------------------------------
# Capture state
# ---------------------------------------------------------------------------
_captured: list[tuple[str, object]] = []
_qiskit_analytic_hits: list[str] = []
_qpanda3_analytic_hits: list[str] = []
_qpanda3_run_attempted: list[bool] = []
_qiskit_capture_committed: bool = False


def _reset_qiskit_capture_cycle() -> None:
    global _qiskit_capture_committed
    _qiskit_capture_committed = False


def _add_qiskit(circ) -> bool:
    try:
        from qiskit import QuantumCircuit
        from qiskit.circuit import Instruction
        if isinstance(circ, QuantumCircuit):
            _captured.append(("qiskit", circ))
            return True
        elif isinstance(circ, Instruction):
            qc = QuantumCircuit(circ.num_qubits, circ.num_clbits)
            qc.append(circ, list(range(circ.num_qubits)), list(range(circ.num_clbits)))
            _captured.append(("qiskit", qc))
            return True
    except Exception:
        pass
    return False


def _add_cirq(circ) -> None:
    try:
        import cirq
        if isinstance(circ, cirq.Circuit):
            _captured.append(("cirq", circ))
    except Exception:
        pass


def _add_qpanda3(prog) -> None:
    try:
        from pyqpanda3.core import QProg, QCircuit
        if isinstance(prog, (QProg, QCircuit)):
            _captured.append(("qpanda3", prog))
    except Exception:
        pass


def _add_pennylane(script) -> None:
    try:
        import io
        import contextlib

        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
        if isinstance(script, qml.tape.QuantumScript):
            _captured.append(("pennylane", script))
    except Exception:
        pass


class _StoppedExecution(Exception):
    pass


# ---------------------------------------------------------------------------
# Qiskit hooks  (Type B: Statevector / DensityMatrix interception)
# ---------------------------------------------------------------------------
_qiskit_class_originals: dict[tuple[type, str], object] = {}
_qiskit_module_originals: list[tuple] = []


def _patch_class(cls, method, replacement) -> None:
    desc = cls.__dict__.get(method)
    _qiskit_class_originals[(cls, method)] = desc
    setattr(cls, method, replacement)


def _patch_module(module, attr, replacement) -> None:
    _qiskit_module_originals.append((module, attr, getattr(module, attr)))
    setattr(module, attr, replacement)


def patch_qiskit() -> None:
    if _qiskit_class_originals or _qiskit_module_originals:
        return

    try:
        from qiskit.quantum_info import Statevector

        def _hooked_sv(cls, instruction):
            global _qiskit_capture_committed
            if not _qiskit_capture_committed and _add_qiskit(instruction):
                _qiskit_capture_committed = True
            raise _StoppedExecution()

        _patch_class(Statevector, "from_instruction", classmethod(_hooked_sv))
    except Exception:
        pass

    try:
        from qiskit.quantum_info import DensityMatrix

        def _hooked_dm(cls, instruction):
            global _qiskit_capture_committed
            if not _qiskit_capture_committed and _add_qiskit(instruction):
                _qiskit_capture_committed = True
            raise _StoppedExecution()

        _patch_class(DensityMatrix, "from_instruction", classmethod(_hooked_dm))
    except Exception:
        pass

    def _make_analytic_hook(name):
        def hooked(*_a, **_kw):
            _qiskit_analytic_hits.append(name)
            raise _StoppedExecution()
        return hooked

    try:
        import qiskit.quantum_info as qi
        for fname in (
            "random_density_matrix",
            "random_statevector",
            "random_unitary",
            "schmidt_decomposition",
        ):
            if hasattr(qi, fname):
                _patch_module(qi, fname, _make_analytic_hook(fname))
    except Exception:
        pass

    try:
        from qiskit.transpiler import PassManager
        _patch_class(PassManager, "run", lambda self, circuits, *a, **kw: circuits)
    except Exception:
        pass
    try:
        from qiskit.transpiler import StagedPassManager
        _patch_class(StagedPassManager, "run", lambda self, circuits, *a, **kw: circuits)
    except Exception:
        pass


def unpatch_qiskit() -> None:
    for (cls, method), desc in _qiskit_class_originals.items():
        if desc is None:
            try:
                delattr(cls, method)
            except Exception:
                pass
        else:
            setattr(cls, method, desc)
    _qiskit_class_originals.clear()
    while _qiskit_module_originals:
        mod, attr, orig = _qiskit_module_originals.pop()
        setattr(mod, attr, orig)


# ---------------------------------------------------------------------------
# Cirq hooks
# ---------------------------------------------------------------------------
_cirq_originals: dict[tuple[type, str], object] = {}


def patch_cirq() -> None:
    if _cirq_originals:
        return
    import cirq

    targets = [
        (cirq.Simulator, "simulate"),
        (cirq.Simulator, "run"),
        (cirq.Simulator, "run_sweep"),
        (cirq.DensityMatrixSimulator, "simulate"),
        (cirq.DensityMatrixSimulator, "run"),
    ]
    for cls, method in targets:
        if not hasattr(cls, method):
            continue
        original = getattr(cls, method)
        _cirq_originals[(cls, method)] = original

        def make_hook(orig):
            def hooked(self, program, *args, **kwargs):
                _add_cirq(program)
                raise _StoppedExecution()
            return hooked

        setattr(cls, method, make_hook(original))


def unpatch_cirq() -> None:
    for (cls, method), orig in _cirq_originals.items():
        setattr(cls, method, orig)
    _cirq_originals.clear()


# ---------------------------------------------------------------------------
# QPanda3 hooks
# ---------------------------------------------------------------------------
_qpanda3_originals: dict[tuple[type, str], object] = {}


class _FakeQpanda3Result:
    def get_counts(self):
        return {"0000": 1}

    def get_prob_list(self):
        return [1.0]

    def get_prob_dict(self, *a, **kw):
        return {"0": 1.0}

    def get_state_vector(self):
        return [1.0 + 0j] + [0.0 + 0j] * 15


def patch_qpanda3() -> None:
    if _qpanda3_originals:
        return

    try:
        from pyqpanda3.core import CPUQVM
        if not hasattr(CPUQVM, "_zxv_orig_run"):
            CPUQVM._zxv_orig_run = CPUQVM.run
            original_run = CPUQVM.run
            _qpanda3_originals[(CPUQVM, "run")] = original_run

            def _cpuqvm_run_hook(self, prog, shots=1000, *args, **kwargs):
                _qpanda3_run_attempted.append(True)
                _add_qpanda3(prog)
                self._fake_result = _FakeQpanda3Result()
                return self

            CPUQVM.run = _cpuqvm_run_hook

            CPUQVM._zxv_orig_result = CPUQVM.result if hasattr(CPUQVM, "result") else None

            def _cpuqvm_result_hook(self):
                if hasattr(self, "_fake_result"):
                    return self._fake_result
                return _FakeQpanda3Result()

            CPUQVM.result = _cpuqvm_result_hook
            _qpanda3_originals[(CPUQVM, "result")] = CPUQVM._zxv_orig_result
    except Exception:
        pass

    try:
        from pyqpanda3.transpilation import Transpiler
        if not hasattr(Transpiler, "_zxv_orig_transpile"):
            Transpiler._zxv_orig_transpile = Transpiler.transpile
            _qpanda3_originals[(Transpiler, "transpile")] = Transpiler._zxv_orig_transpile

            def _transpile_identity(self, prog, *args, **kwargs):
                return prog

            Transpiler.transpile = _transpile_identity
    except Exception:
        pass

    try:
        from pyqpanda3.core import QCircuit
        if not hasattr(QCircuit, "_zxv_orig_matrix"):
            QCircuit._zxv_orig_matrix = QCircuit.matrix
            _qpanda3_originals[(QCircuit, "matrix")] = QCircuit._zxv_orig_matrix

            def _matrix_hook(self, *args, **kwargs):
                _qpanda3_analytic_hits.append("QCircuit.matrix")
                return QCircuit._zxv_orig_matrix(self, *args, **kwargs)

            QCircuit.matrix = _matrix_hook
    except Exception:
        pass


def unpatch_qpanda3() -> None:
    for (cls, method), orig in _qpanda3_originals.items():
        if orig is not None:
            setattr(cls, method, orig)
        if hasattr(cls, f"_zxv_orig_{method}"):
            try:
                delattr(cls, f"_zxv_orig_{method}")
            except Exception:
                pass
    _qpanda3_originals.clear()


# ---------------------------------------------------------------------------
# PennyLane hooks
# ---------------------------------------------------------------------------
_pennylane_originals: dict[tuple[type, str], object] = {}


def _capture_pennylane_from(value) -> None:
    try:
        import io
        import contextlib

        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
        if isinstance(value, qml.tape.QuantumScript):
            _add_pennylane(value)
        elif isinstance(value, qml.QNode):
            _add_pennylane(qml.workflow.construct_tape(value)())
    except Exception:
        pass


def patch_pennylane() -> None:
    if _pennylane_originals:
        return
    try:
        import io
        import contextlib

        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
        original = qml.QNode.__call__
        _pennylane_originals[(qml.QNode, "__call__")] = original

        def _hooked_qnode_call(self, *args, **kwargs):
            script = qml.workflow.construct_tape(self)(*args, **kwargs)
            _add_pennylane(script)
            raise _StoppedExecution()

        qml.QNode.__call__ = _hooked_qnode_call
    except Exception:
        pass


def unpatch_pennylane() -> None:
    for (cls, method), orig in _pennylane_originals.items():
        setattr(cls, method, orig)
    _pennylane_originals.clear()


# ---------------------------------------------------------------------------
# Default argument fixtures
# ---------------------------------------------------------------------------
def _bell_qiskit_nomeas():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def _bell_cirq_nomeas():
    import cirq
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))


def _bell_qpanda3_nomeas():
    from pyqpanda3.core import QCircuit, H, CNOT
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)
    return qc


def _bell_pennylane_nomeas():
    import io
    import contextlib

    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        import pennylane as qml
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
    return tape


def _bell_state_array():
    import numpy as np
    return np.array([1.0, 0.0, 0.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)


# ---------------------------------------------------------------------------
# Function-name -> argument candidates registry
# ---------------------------------------------------------------------------
FUNCTION_ARG_CANDIDATES: dict[str, list[tuple]] = {
    "get_statevector":              [("bell_circuit",)],
    "create_uniform_superposition": [(3,)],
    "pure_states":                  [(0.9,)],
    "entanglement_dataset":         [(0.1,)],
    "mutual_information_dataset":   [(0.1,)],
    "schmidt_test":                 [("bell_state", [1])],
    "purity_dataset":               [()],
    "fidelity_dataset":             [()],
    "concurrence_dataset":          [()],
}

# Generic fallback candidates tried in order for unknown function names
_FALLBACK_ARG_CANDIDATES: list[tuple] = [
    (),
    (3,),
    (0.5,),
    ("bell_circuit",),
    (4,),
    (0.1,),
    (0.9,),
]


def resolve_args(arg_spec: tuple, framework: str) -> tuple:
    out = []
    for s in arg_spec:
        if s == "bell_circuit":
            if framework == "qiskit":
                out.append(_bell_qiskit_nomeas())
            elif framework == "cirq":
                out.append(_bell_cirq_nomeas())
            elif framework == "pennylane":
                out.append(_bell_pennylane_nomeas())
            else:
                out.append(_bell_qpanda3_nomeas())
        elif s == "bell_state":
            out.append(_bell_state_array())
        else:
            out.append(s)
    return tuple(out)


def _as_arg_spec_candidates(arg_spec) -> list[tuple]:
    if isinstance(arg_spec, list):
        return [tuple(s) for s in arg_spec] if arg_spec else [()]
    return [tuple(arg_spec)]


# ---------------------------------------------------------------------------
# Module loader + framework detection
# ---------------------------------------------------------------------------
def load_module(filepath: str, name: str):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        spec.loader.exec_module(mod)
    return mod


def detect_framework(filepath: str) -> str:
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return "qiskit"

    has_cirq    = ("import cirq"      in content) or ("from cirq"      in content)
    has_qiskit  = ("import qiskit"    in content) or ("from qiskit"    in content)
    has_qpanda3 = ("import pyqpanda3" in content) or ("from pyqpanda3" in content)
    has_pennylane = ("import pennylane" in content) or ("from pennylane" in content)

    if has_pennylane and not has_qpanda3 and not has_cirq and not has_qiskit:
        return "pennylane"
    if has_qpanda3 and not has_cirq and not has_qiskit:
        return "qpanda3"
    if has_cirq and not has_qiskit and not has_qpanda3:
        return "cirq"
    if has_qiskit and not has_cirq and not has_qpanda3:
        return "qiskit"

    positions: dict[str, int] = {}
    if has_qpanda3:
        positions["qpanda3"] = min(
            (p for p in (content.find("import pyqpanda3"), content.find("from pyqpanda3")) if p >= 0),
            default=10**9,
        )
    if has_pennylane:
        positions["pennylane"] = min(
            (p for p in (content.find("import pennylane"), content.find("from pennylane")) if p >= 0),
            default=10**9,
        )
    if has_cirq:
        positions["cirq"] = min(
            (p for p in (content.find("import cirq"), content.find("from cirq")) if p >= 0),
            default=10**9,
        )
    if has_qiskit:
        positions["qiskit"] = min(
            (p for p in (content.find("import qiskit"), content.find("from qiskit")) if p >= 0),
            default=10**9,
        )
    if positions:
        return min(positions, key=positions.__getitem__)
    return "qiskit"


def _unique_modname(filepath: str, framework: str) -> str:
    return f"{framework}_prog_{Path(filepath).stem}"


# ---------------------------------------------------------------------------
# Circuit -> QASM -> pyzx
# ---------------------------------------------------------------------------
PYZX_BASIS = [
    "cx", "cz", "h", "x", "y", "z", "s", "sdg", "t", "tdg",
    "rx", "ry", "rz", "u1", "u2", "u3", "p", "ccx", "swap",
]


def qiskit_to_qasm(qcirc) -> str:
    from qiskit import QuantumCircuit, qasm2, transpile

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


def cirq_to_qasm(ccirc) -> str:
    import cirq

    all_qubits = sorted(ccirc.all_qubits())

    def _is_noise(op) -> bool:
        gate = getattr(op, "gate", None)
        if gate is None:
            return False
        if isinstance(gate, getattr(cirq, "ResetChannel", ())):
            return True
        if hasattr(cirq, "is_measurement") and cirq.is_measurement(op):
            return True
        try:
            return not cirq.has_unitary(op)
        except Exception:
            return False

    ops = []
    for op in ccirc.all_operations():
        if cirq.is_measurement(op):
            continue
        if _is_noise(op):
            continue
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
    filtered = [
        line for line in lines
        if not line.strip().startswith("measure") and not line.strip().startswith("creg")
    ]
    return "\n".join(filtered)


def pennylane_to_qasm(script) -> str:
    import io
    import contextlib

    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        import pennylane as qml
    qasm_raw = qml.to_openqasm(script)
    if callable(qasm_raw):
        qasm_raw = qasm_raw()
    filtered = [
        line for line in str(qasm_raw).splitlines()
        if not line.strip().startswith("measure") and not line.strip().startswith("creg")
    ]
    return "\n".join(filtered)


def zx_equivalent(qasm_a: str, qasm_b: str) -> tuple[bool | None, str]:
    import pyzx as zx

    try:
        ca = zx.Circuit.from_qasm(qasm_a)
        cb = zx.Circuit.from_qasm(qasm_b)
    except Exception as e:
        return None, f"qasm parse: {e}"

    if ca.qubits != cb.qubits:
        return False, f"qubit count mismatch {ca.qubits} vs {cb.qubits}"

    try:
        eq = ca.verify_equality(cb, up_to_global_phase=True)
        return bool(eq), ""
    except Exception as e:
        return None, f"verify_equality failed: {e}"


# ---------------------------------------------------------------------------
# Framework-specific capture helpers
# ---------------------------------------------------------------------------
def capture_qiskit_generic(
    filepath: str, fn_name: str, arg_spec
) -> tuple[list, list[str]]:
    """Returns (circuits, analytic_hits)."""
    _captured.clear()
    _qiskit_analytic_hits.clear()
    _reset_qiskit_capture_cycle()
    patch_qiskit()
    mod_name = _unique_modname(filepath, "qiskit")
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception:
            mod = sys.modules.get(mod_name)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            for spec in _as_arg_spec_candidates(arg_spec):
                before_c = len(_captured)
                before_a = len(_qiskit_analytic_hits)
                args = resolve_args(spec, "qiskit")
                try:
                    with contextlib.redirect_stdout(io.StringIO()), \
                         contextlib.redirect_stderr(io.StringIO()):
                        fn(*args)
                except _StoppedExecution:
                    pass
                except Exception:
                    pass
                if len(_captured) > before_c or len(_qiskit_analytic_hits) > before_a:
                    break
    finally:
        unpatch_qiskit()
    return list(_captured), list(_qiskit_analytic_hits)


def capture_cirq_generic(
    filepath: str, fn_name: str, arg_spec
) -> list:
    _captured.clear()
    patch_cirq()
    mod_name = _unique_modname(filepath, "cirq")
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception:
            mod = sys.modules.get(mod_name)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            for spec in _as_arg_spec_candidates(arg_spec):
                before_c = len(_captured)
                args = resolve_args(spec, "cirq")
                try:
                    with contextlib.redirect_stdout(io.StringIO()), \
                         contextlib.redirect_stderr(io.StringIO()):
                        fn(*args)
                except _StoppedExecution:
                    pass
                except Exception:
                    pass
                if len(_captured) > before_c:
                    break
    finally:
        unpatch_cirq()
    return list(_captured)


def capture_qpanda3_generic(
    filepath: str, fn_name: str, arg_spec
) -> tuple[list, list[str]]:
    _captured.clear()
    _qpanda3_analytic_hits.clear()
    _qpanda3_run_attempted.clear()
    patch_qpanda3()
    mod_name = _unique_modname(filepath, "qpanda3")
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception:
            mod = sys.modules.get(mod_name)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            for spec in _as_arg_spec_candidates(arg_spec):
                before_c = len(_captured)
                args = resolve_args(spec, "qpanda3")
                try:
                    with contextlib.redirect_stdout(io.StringIO()), \
                         contextlib.redirect_stderr(io.StringIO()):
                        fn(*args)
                except _StoppedExecution:
                    pass
                except Exception:
                    pass
                if len(_captured) > before_c:
                    break
    finally:
        unpatch_qpanda3()
    # Only report analytic hits when CPUQVM.run was never called.
    # If run was attempted but capture failed, that is a genuine CAPTURE_FAIL.
    analytic = [] if _qpanda3_run_attempted else list(_qpanda3_analytic_hits)
    return list(_captured), analytic


def capture_pennylane_generic(
    filepath: str, fn_name: str, arg_spec
) -> tuple[list, list[str]]:
    _captured.clear()
    patch_pennylane()
    mod_name = _unique_modname(filepath, "pennylane")
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception:
            mod = sys.modules.get(mod_name)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            for spec in _as_arg_spec_candidates(arg_spec):
                before_c = len(_captured)
                args = resolve_args(spec, "pennylane")
                try:
                    with contextlib.redirect_stdout(io.StringIO()), \
                         contextlib.redirect_stderr(io.StringIO()):
                        ret = fn(*args)
                    _capture_pennylane_from(ret)
                except _StoppedExecution:
                    pass
                except Exception:
                    pass
                if len(_captured) > before_c:
                    break
    finally:
        unpatch_pennylane()
    return list(_captured), []


def _capture_by_framework(
    framework: str, filepath: str, fn_name: str, arg_spec
) -> tuple[list, list[str]]:
    """Unified dispatch. Always returns (circuits, analytic_hits)."""
    if framework == "qiskit":
        return capture_qiskit_generic(filepath, fn_name, arg_spec)
    elif framework == "cirq":
        return capture_cirq_generic(filepath, fn_name, arg_spec), []
    elif framework == "qpanda3":
        return capture_qpanda3_generic(filepath, fn_name, arg_spec)
    elif framework == "pennylane":
        return capture_pennylane_generic(filepath, fn_name, arg_spec)
    else:
        raise ValueError(f"unsupported framework: {framework}")


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------
def _compare_captured(circs_a: list, circs_b: list) -> tuple[str, str]:
    if len(circs_a) != len(circs_b):
        return (
            "CAPTURE_COUNT_MISMATCH",
            f"captured a={len(circs_a)} b={len(circs_b)}",
        )

    n = len(circs_a)
    flags: list[bool | None] = []
    notes: list[str] = []

    for i in range(n):
        fw_a, circ_a = circs_a[i]
        fw_b, circ_b = circs_b[i]

        try:
            if fw_a == "qiskit":
                qasm_a = qiskit_to_qasm(circ_a)
            elif fw_a == "cirq":
                qasm_a = cirq_to_qasm(circ_a)
            elif fw_a == "qpanda3":
                qasm_a = qpanda3_to_qasm(circ_a)
            elif fw_a == "pennylane":
                qasm_a = pennylane_to_qasm(circ_a)
            else:
                raise ValueError(f"unknown framework: {fw_a}")
        except Exception as e:
            flags.append(None)
            notes.append(f"#{i} A-qasm: {e}")
            continue

        try:
            if fw_b == "qiskit":
                qasm_b = qiskit_to_qasm(circ_b)
            elif fw_b == "cirq":
                qasm_b = cirq_to_qasm(circ_b)
            elif fw_b == "qpanda3":
                qasm_b = qpanda3_to_qasm(circ_b)
            elif fw_b == "pennylane":
                qasm_b = pennylane_to_qasm(circ_b)
            else:
                raise ValueError(f"unknown framework: {fw_b}")
        except Exception as e:
            flags.append(None)
            notes.append(f"#{i} B-qasm: {e}")
            continue

        eq, err = zx_equivalent(qasm_a, qasm_b)
        flags.append(eq)
        if err:
            notes.append(f"#{i} {err}")

    if flags and all(f is True for f in flags):
        status = "EQUIVALENT"
    else:
        status = "NOT_PROVED"

    flags_str = f" flags={flags}" if any(f is not None for f in flags) else ""
    detail = (
        f"captured a={len(circs_a)} b={len(circs_b)}{flags_str}"
        + (f" | {' ; '.join(notes)}" if notes else "")
    )
    return status, detail


# ---------------------------------------------------------------------------
# Flexible pair runner  (all 6 framework combinations)
# ---------------------------------------------------------------------------
def run_pair_flexible(
    idx: int,
    file_a: str,
    file_b: str,
    prog_a: dict | None = None,
    prog_b: dict | None = None,
    framework_a: str | None = None,
    framework_b: str | None = None,
) -> dict:
    if prog_a is None:
        inferred_a = _infer_program_entry_from_file(Path(file_a))
        prog_a = {idx: inferred_a} if inferred_a is not None else {}
    if prog_b is None:
        inferred_b = _infer_program_entry_from_file(Path(file_b))
        prog_b = {idx: inferred_b} if inferred_b is not None else {}

    if idx not in prog_a or idx not in prog_b:
        detail = []
        if idx not in prog_a:
            detail.append("A: no runnable entry function detected")
        if idx not in prog_b:
            detail.append("B: no runnable entry function detected")
        return {"idx": idx, "status": "UNSUPPORTED", "detail": " ; ".join(detail)}

    fw_a = framework_a or detect_framework(file_a)
    fw_b = framework_b or detect_framework(file_b)
    fn_a, spec_a = prog_a[idx]
    fn_b, spec_b = prog_b[idx]

    out = {"idx": idx, "status": "PENDING", "detail": ""}

    try:
        circs_a, analytic_a = _capture_by_framework(fw_a, file_a, fn_a, spec_a)
    except Exception as e:
        out["status"] = "ERROR"
        out["detail"] = f"A-side load: {e}"
        return out

    try:
        circs_b, analytic_b = _capture_by_framework(fw_b, file_b, fn_b, spec_b)
    except Exception as e:
        out["status"] = "ERROR"
        out["detail"] = f"B-side load: {e}"
        return out

    # Check both sides together so that analytic detection on either side
    # (currently only Qiskit has analytic hooks) prevents a false CAPTURE_FAIL
    # when the frameworks are swapped.
    if not circs_a or not circs_b:
        if analytic_a or analytic_b:
            parts = []
            if analytic_a:
                parts.append(
                    f"A-side uses analytical API "
                    f"({', '.join(sorted(set(analytic_a)))}) — no QuantumCircuit to compare"
                )
            if analytic_b:
                parts.append(
                    f"B-side uses analytical API "
                    f"({', '.join(sorted(set(analytic_b)))}) — no QuantumCircuit to compare"
                )
            out["status"] = "NOT_APPLICABLE"
            out["detail"] = " ; ".join(parts)
        else:
            parts = []
            if not circs_a:
                parts.append("A-side: no circuit captured")
            if not circs_b:
                parts.append("B-side: no circuit captured")
            out["status"] = "CAPTURE_FAIL"
            out["detail"] = " ; ".join(parts)
        return out

    out["status"], out["detail"] = _compare_captured(circs_a, circs_b)
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
            start = int(a.strip())
            end   = int(b.strip())
            step  = 1 if end >= start else -1
            parsed.extend(range(start, end + step, step))
        else:
            parsed.append(int(token))

    unique: list[int] = []
    seen: set[int] = set()
    for idx in parsed:
        if idx in seen:
            continue
        seen.add(idx)
        unique.append(idx)
    return unique


def _compile_idx_pattern(pattern: str) -> re.Pattern:
    if "{idx}" not in pattern:
        raise ValueError("pattern must contain '{idx}' placeholder")
    regex_text = "^" + re.escape(pattern).replace(r"\{idx\}", r"(?P<idx>\d+)") + "$"
    return re.compile(regex_text)


def _discover_indices_from_dir(directory: Path, pattern: str) -> set[int]:
    regex = _compile_idx_pattern(pattern)
    found: set[int] = set()
    for entry in directory.iterdir():
        if not entry.is_file():
            continue
        m = regex.match(entry.name)
        if m:
            found.add(int(m.group("idx")))
    return found


def _discover_paired_indices(
    dir_a: Path, pattern_a: str, dir_b: Path, pattern_b: str
) -> list[int]:
    return sorted(
        _discover_indices_from_dir(dir_a, pattern_a)
        & _discover_indices_from_dir(dir_b, pattern_b)
    )


def _infer_program_entry_from_file(filepath: Path) -> tuple[str, list[tuple]] | None:
    try:
        src = filepath.read_text(encoding="utf-8-sig", errors="replace")
        tree = ast.parse(src, filename=str(filepath))
    except Exception:
        return None

    defs_in_order = [
        node.name for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    for name in defs_in_order:
        if name in FUNCTION_ARG_CANDIDATES:
            return name, FUNCTION_ARG_CANDIDATES[name]

    # Fallback: first non-private top-level function with generic candidates
    for name in defs_in_order:
        if not name.startswith("_"):
            return name, _FALLBACK_ARG_CANDIDATES
    return None


def _resolve_program_entry(
    filepath: Path,
) -> tuple[tuple[str, list[tuple]] | None, str]:
    inferred = _infer_program_entry_from_file(filepath)
    if inferred is not None:
        fn, _ = inferred
        return inferred, f"function `{fn}`"
    return None, "no known Type-B entry function found in file"


def _resolve_path(base: Path, path_like: str) -> Path:
    p = Path(path_like)
    if not p.is_absolute():
        p = base / p
    return p


# ---------------------------------------------------------------------------
# Status text mapping (English report)
# ---------------------------------------------------------------------------
STATUS_EN: dict[str, str] = {
    "EQUIVALENT":             "Equivalent",
    "NOT_PROVED":             "Not Proved",
    "NOT_APPLICABLE":         "Not Applicable (Analytical API)",
    "ERROR":                  "Error",
    "CAPTURE_FAIL":           "Capture Failed",
    "MISSING":                "File Missing",
    "MIXED":                  "Mixed Results",
    "UNSUPPORTED":            "Unsupported",
    "PENDING":                "Pending",
    "CAPTURE_COUNT_MISMATCH": "Circuit Count Mismatch",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> None:
    from zx_unified import legacy_main
    return legacy_main("type2", globals(), argv)

    parser = argparse.ArgumentParser(
        description=(
            "ZX equivalence verifier — Type B quantum programs "
            "(statevector/quantum-state output). "
            "Supports qiskit / cirq / Qpanda3, 6 framework combinations."
        )
    )
    parser.add_argument("--dir-a",       default="class2/codes",
                        help="Directory of side A files")
    parser.add_argument("--dir-b",       default="Qclass2",
                        help="Directory of side B files")
    parser.add_argument("--pattern-a",   default="code{idx}.py",
                        help="Filename template for side A (must include {idx})")
    parser.add_argument("--pattern-b",   default="llmQpanda{idx}.py",
                        help="Filename template for side B (must include {idx})")
    parser.add_argument("--framework-a", choices=["auto", "qiskit", "cirq", "Qpanda3"],
                        default="auto",
                        help="Framework of side A (auto = detect from imports)")
    parser.add_argument("--framework-b", choices=["auto", "qiskit", "cirq", "Qpanda3"],
                        default="auto",
                        help="Framework of side B (auto = detect from imports)")
    parser.add_argument("--indices",     default="all",
                        help="Index selection: all  or  e.g. 11,39,136-139")
    parser.add_argument("--out",         default="type2-result.md",
                        help="Output Markdown report path")
    parser.add_argument("--path-add",    action="append", default=[],
                        help="Extra import path (repeatable)")
    args = parser.parse_args(argv)

    def _norm_fw(fw_str: str) -> str | None:
        if fw_str == "auto":
            return None
        return fw_str.lower()   # Qpanda3 -> qpanda3

    base        = Path(__file__).resolve().parent
    dir_a       = _resolve_path(base, args.dir_a)
    dir_b       = _resolve_path(base, args.dir_b)
    out_path    = _resolve_path(base, args.out)
    extra_paths = [_resolve_path(base, p) for p in args.path_add]

    if not dir_a.exists() or not dir_a.is_dir():
        parser.error(f"--dir-a is not a valid directory: {dir_a}")
    if not dir_b.exists() or not dir_b.is_dir():
        parser.error(f"--dir-b is not a valid directory: {dir_b}")

    for p in [base, dir_a.parent, dir_b.parent, dir_a, dir_b, *extra_paths]:
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)

    try:
        if not args.indices or args.indices.lower() in ("all", "*"):
            discovered = _discover_paired_indices(
                dir_a, args.pattern_a, dir_b, args.pattern_b
            )
            if not discovered:
                parser.error(
                    "no paired files found under dir-a/dir-b "
                    "matching pattern-a/pattern-b"
                )
            indices = discovered
        else:
            indices = _parse_indices(args.indices)
    except ValueError as e:
        parser.error(str(e))

    fw_a = _norm_fw(args.framework_a)
    fw_b = _norm_fw(args.framework_b)

    results: list[dict] = []
    for idx in indices:
        try:
            name_a = args.pattern_a.format(idx=idx)
            name_b = args.pattern_b.format(idx=idx)
        except KeyError as e:
            parser.error(f"pattern contains unsupported placeholder: {e}")

        file_a = dir_a / name_a
        file_b = dir_b / name_b
        if not file_a.exists() or not file_b.exists():
            missing = []
            if not file_a.exists():
                missing.append(f"A:{file_a}")
            if not file_b.exists():
                missing.append(f"B:{file_b}")
            results.append({"idx": idx, "status": "MISSING", "detail": "; ".join(missing)})
            continue

        entry_a, note_a = _resolve_program_entry(file_a)
        entry_b, note_b = _resolve_program_entry(file_b)
        if entry_a is None or entry_b is None:
            reason = []
            if entry_a is None:
                reason.append(f"A: {note_a}")
            if entry_b is None:
                reason.append(f"B: {note_b}")
            results.append({"idx": idx, "status": "UNSUPPORTED", "detail": " ; ".join(reason)})
            print(f"[{idx:>3}]  {'UNSUPPORTED':<24}  {' ; '.join(reason)[:180]}")
            continue

        prog_a = {idx: entry_a}
        prog_b = {idx: entry_b}
        r = run_pair_flexible(
            idx,
            str(file_a),
            str(file_b),
            prog_a,
            prog_b,
            framework_a=fw_a,
            framework_b=fw_b,
        )
        results.append(r)
        print(f"[{idx:>3}]  {r['status']:<24}  {r['detail'][:180]}")

    n_eq  = sum(1 for r in results if r["status"] == "EQUIVALENT")
    n_ne  = sum(1 for r in results if r["status"] == "NOT_PROVED")
    n_na  = sum(1 for r in results if r["status"] == "NOT_APPLICABLE")
    n_err = sum(1 for r in results if r["status"] in (
        "ERROR", "CAPTURE_FAIL", "MISSING", "MIXED", "UNSUPPORTED", "CAPTURE_COUNT_MISMATCH"
    ))

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# ZX Equivalence Verification Report — Type B Quantum Programs\n\n")
        f.write(f"**Side A:** `{args.dir_a}/{args.pattern_a}`  \n")
        f.write(f"**Side B:** `{args.dir_b}/{args.pattern_b}`  \n")
        f.write(
            f"**Framework Mode:** A=`{args.framework_a}`, B=`{args.framework_b}` "
            f"(`auto` = detected from imports)\n\n"
        )
        f.write(
            "**Method:** Intercept statevector/density-matrix simulation entry points "
            "(Qiskit `Statevector.from_instruction` / `DensityMatrix.from_instruction`, "
            "Cirq `Simulator.simulate` / `run`, "
            "QPanda3 `CPUQVM.run`) to capture user-written quantum circuits; "
            "strip non-unitary operations (measurements, resets, barriers); "
            "convert to OpenQASM 2.0, then compare ZX-circuit equality via "
            "`Circuit.verify_equality(..., up_to_global_phase=True)`. "
            "Programs that rely solely on analytical APIs (e.g. `random_density_matrix`, "
            "`random_statevector`) without constructing an explicit quantum circuit are marked "
            "**Not Applicable**.\n\n"
        )
        f.write(
            f"**Summary:** Equivalent = {n_eq} / {len(results)}, "
            f"Not Proved = {n_ne}, "
            f"Not Applicable = {n_na}, "
            f"Failure = {n_err}.\n\n"
        )
        f.write("| Index | ZX Equivalence Result | Notes |\n")
        f.write("|:-----:|:---------------------:|:------|\n")
        for r in results:
            en_status = STATUS_EN.get(r["status"], r["status"])
            d = r["detail"].replace("|", "\\|").replace("\n", " ")
            if len(d) > 300:
                d = d[:300] + "..."
            f.write(f"| {r['idx']} | {en_status} | {d} |\n")

    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
