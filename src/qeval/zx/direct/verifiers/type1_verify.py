"""
type1-three.py

ZX绛変环鎬ч獙璇佸櫒锛屾敮鎸?Type A 閲忓瓙绋嬪簭锛堟?鐜囧垎甯冭緭鍑虹被鍨嬶級銆?鏀?寔6绉嶆?鏋剁粍鍚堬細
  qiskit-qiskit, cirq-cirq, qiskit-cirq,
  Qpanda3-Qpanda3, cirq-Qpanda3, qiskit-Qpanda3

绛栫暐锛堟嫤鎴?墽琛?+ 鍓ョ?娴嬮噺锛夛細
  1. 瀵?qiskit/cirq/Qpanda3 鐨勬ā鎷熷櫒鍏ュ彛杩涜? monkey-patch锛屾崟鑾烽噺瀛愮嚎璺??璞°€?  2. 鍓ラ櫎娴嬮噺/閲嶇疆/barrier/缁忓吀鏉′欢闂ㄧ瓑闈為厜鎿嶄綔銆?  3. 杞?崲涓?OpenQASM 2.0锛屾瀯寤?pyzx 绾胯矾 -> ZX 鍥俱€?  4. 閫氳繃 pyzx.compare_tensors锛坧reserve_scalar=False锛夎繘琛岀瓑浠锋€ф瘮杈冦€?
CLI 鐢ㄦ硶锛?  python type1-three.py \
    --dir-a <鐩?綍A> --pattern-a '<妯℃澘A鍚珄idx}>' --framework-a <auto|qiskit|cirq|Qpanda3> \
    --dir-b <鐩?綍B> --pattern-b '<妯℃澘B鍚珄idx}>' --framework-b <auto|qiskit|cirq|Qpanda3> \
    --indices <all鎴栫紪鍙峰垪琛? \
    --out <鎶ュ憡鍚?md>
"""





from __future__ import annotations

import argparse
import ast
import importlib.util
import math
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    matplotlib = None

# ---------------------------------------------------------------------------
# 鎹曡幏鐘舵€?# ---------------------------------------------------------------------------
_captured: list[tuple[str, object]] = []
_capture_sources: list[str] = []
_capture_policy: dict[str, object] = {"stop_after_hook": False}


@dataclass
class CaptureOutcome:
    circuits: list[tuple[str, object]]
    sources: list[str]
    error: str | None = None


def _add_qiskit(circ, source: str = "unknown") -> None:
    try:
        from qiskit import QuantumCircuit
        if isinstance(circ, QuantumCircuit):
            _captured.append(("qiskit", circ))
            _capture_sources.append(source)
    except Exception:
        pass


def _add_cirq(circ, source: str = "cirq.run") -> None:
    try:
        import cirq
        if isinstance(circ, cirq.Circuit):
            _captured.append(("cirq", circ))
            _capture_sources.append(source)
    except Exception:
        pass


def _add_qpanda3(prog, source: str = "qpanda3.run") -> None:
    try:
        from pyqpanda3.core import QProg, QCircuit
        if isinstance(prog, (QProg, QCircuit)):
            _captured.append(("qpanda3", prog))
            _capture_sources.append(source)
    except Exception:
        pass


def _add_pennylane(script, source: str = "pennylane.qnode") -> None:
    try:
        import io
        import contextlib

        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
        if isinstance(script, qml.tape.QuantumScript):
            _captured.append(("pennylane", script))
            _capture_sources.append(source)
    except Exception:
        pass


class _StoppedExecution(Exception):
    pass


class NonUnitaryCirqOperationError(ValueError):
    pass


def _reset_capture(policy: dict[str, object] | None = None) -> None:
    _captured.clear()
    _capture_sources.clear()
    _capture_policy.clear()
    _capture_policy.update(policy or {"stop_after_hook": False})


def _stop_after_hook() -> bool:
    return bool(_capture_policy.get("stop_after_hook", False))


def _collect_all_circuits() -> bool:
    return bool(_capture_policy.get("collect_all_circuits", False))


def _maybe_stop_after_hook() -> None:
    if _stop_after_hook() and _captured:
        raise _StoppedExecution()


def _iter_qiskit_circuits(obj):
    try:
        from qiskit import QuantumCircuit
    except Exception:
        return
    if isinstance(obj, QuantumCircuit):
        yield obj
        return
    if isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from _iter_qiskit_circuits(item)
        return
    if isinstance(obj, dict):
        for item in obj.values():
            yield from _iter_qiskit_circuits(item)


def _capture_qiskit_from(obj, source: str) -> list:
    circuits = list(_iter_qiskit_circuits(obj) or [])
    for circ in circuits:
        _add_qiskit(circ, source)
    return circuits


def _iter_cirq_circuits(obj):
    try:
        import cirq
    except Exception:
        return
    if isinstance(obj, cirq.Circuit):
        yield obj
        return
    if isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from _iter_cirq_circuits(item)
        return
    if isinstance(obj, dict):
        for item in obj.values():
            yield from _iter_cirq_circuits(item)


def _capture_cirq_from(obj, source: str) -> list:
    circuits = list(_iter_cirq_circuits(obj) or [])
    for circ in circuits:
        _add_cirq(circ, source)
    return circuits


def _iter_qpanda3_programs(obj):
    try:
        from pyqpanda3.core import QProg, QCircuit
    except Exception:
        return
    if isinstance(obj, (QProg, QCircuit)):
        yield obj
        return
    if isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from _iter_qpanda3_programs(item)
        return
    if isinstance(obj, dict):
        for item in obj.values():
            yield from _iter_qpanda3_programs(item)


def _capture_qpanda3_from(obj, source: str) -> list:
    programs = list(_iter_qpanda3_programs(obj) or [])
    for prog in programs:
        _add_qpanda3(prog, source)
    return programs


def _iter_pennylane_circuits(obj):
    try:
        import io
        import contextlib

        devnull = io.StringIO()
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import pennylane as qml
    except Exception:
        return
    if isinstance(obj, qml.tape.QuantumScript):
        yield obj
        return
    if isinstance(obj, qml.QNode):
        try:
            yield qml.workflow.construct_tape(obj)()
        except Exception:
            return
        return
    if isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from _iter_pennylane_circuits(item)
        return
    if isinstance(obj, dict):
        for item in obj.values():
            yield from _iter_pennylane_circuits(item)


def _capture_pennylane_from(obj, source: str) -> list:
    circuits = list(_iter_pennylane_circuits(obj) or [])
    for circuit in circuits:
        _add_pennylane(circuit, source)
    return circuits


_pennylane_originals: dict[tuple[type, str], object] = {}


def _pennylane_total_shots(shots_obj) -> int:
    total = getattr(shots_obj, "total_shots", None)
    if total:
        return int(total)
    try:
        return int(shots_obj)
    except Exception:
        return 1


def _fake_pennylane_result(qml, qnode, script):
    import numpy as np

    if not script.measurements:
        return None

    def fake_measurement(measurement):
        name = measurement.__class__.__name__.lower()
        wires = list(getattr(measurement, "wires", []) or getattr(script, "wires", []))
        width = max(len(wires), 1)
        shots = _pennylane_total_shots(getattr(getattr(qnode, "device", None), "shots", None))
        if "sample" in name:
            return np.zeros((shots, width), dtype=int)
        if "counts" in name:
            return {"0" * width: shots}
        if "prob" in name:
            probs = np.zeros(2 ** width, dtype=float)
            probs[0] = 1.0
            return probs
        if "state" in name:
            state = np.zeros(2 ** width, dtype=complex)
            state[0] = 1.0 + 0.0j
            return state
        if "density" in name:
            dm = np.zeros((2 ** width, 2 ** width), dtype=complex)
            dm[0, 0] = 1.0 + 0.0j
            return dm
        return 0.0

    values = [fake_measurement(measurement) for measurement in script.measurements]
    if len(values) == 1:
        return values[0]
    return tuple(values)


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
            _add_pennylane(script, "pennylane.qnode")
            if _stop_after_hook() and _captured:
                raise _StoppedExecution()
            return _fake_pennylane_result(qml, self, script)

        qml.QNode.__call__ = _hooked_qnode_call
    except Exception:
        pass


def unpatch_pennylane() -> None:
    for (cls, method), orig in _pennylane_originals.items():
        setattr(cls, method, orig)
    _pennylane_originals.clear()


# ---------------------------------------------------------------------------
# Qiskit hooks
# ---------------------------------------------------------------------------
_qiskit_originals: dict[tuple[type, str], object] = {}


class _FakeCounts(dict):
    def get_counts(self, *_a, **_kw):
        return dict(self)

    def get_bitstrings(self, *_a, **_kw):
        return [next(iter(self.keys()), "0")] * sum(self.values())


class _FakePubData:
    def __init__(self, n_clbits: int):
        bits = "0" * max(n_clbits, 1)
        counts = _FakeCounts({bits: 1})
        self.meas = counts
        self.c = counts
        self.measure = counts


class _FakePubResult:
    def __init__(self, n_clbits: int):
        self.data = _FakePubData(n_clbits)


class _FakeQiskitResult(list):
    def __init__(self, circuits):
        super().__init__()
        self._counts = []
        for circ in circuits:
            n = getattr(circ, "num_clbits", 0) or getattr(circ, "num_qubits", 1)
            bits = "0" * max(n, 1)
            self._counts.append(_FakeCounts({bits: 1}))
            self.append(_FakePubResult(n))

    def get_counts(self, experiment=None):
        if not self._counts:
            return _FakeCounts({"0": 1})
        if isinstance(experiment, int):
            if 0 <= experiment < len(self._counts):
                return self._counts[experiment]
            return self._counts[0]
        return self._counts[0]


class _FakeQiskitJob:
    def __init__(self, circuits):
        self._result = _FakeQiskitResult(circuits)

    def result(self):
        return self._result


def patch_qiskit() -> None:
    if _qiskit_originals:
        return

    targets: list[tuple[type, str]] = []
    try:
        from qiskit_ibm_runtime import Sampler as RTSampler
        targets.append((RTSampler, "run"))
    except Exception:
        pass
    try:
        from qiskit.primitives import StatevectorSampler
        targets.append((StatevectorSampler, "run"))
    except Exception:
        pass
    try:
        from qiskit.primitives import Sampler as PrimSampler
        targets.append((PrimSampler, "run"))
    except Exception:
        pass
    try:
        from qiskit_aer.primitives import Sampler as AerSampler
        targets.append((AerSampler, "run"))
    except Exception:
        pass
    try:
        from qiskit_aer.primitives import SamplerV2 as AerSamplerV2
        targets.append((AerSamplerV2, "run"))
    except Exception:
        pass

    for cls, method in targets:
        if not hasattr(cls, method):
            continue
        original = getattr(cls, method)
        _qiskit_originals[(cls, method)] = original

        def make_hook(orig):
            def hooked(self, pubs, *args, **kwargs):
                items = pubs if isinstance(pubs, (list, tuple)) else [pubs]
                circuits = []
                for pub in items:
                    if isinstance(pub, tuple):
                        circ = pub[0]
                    else:
                        circ = pub
                    circuits.extend(_capture_qiskit_from(circ, "sampler.run"))
                _maybe_stop_after_hook()
                return _FakeQiskitJob(circuits)
            return hooked

        setattr(cls, method, make_hook(original))

    try:
        from qiskit_aer import AerSimulator
        if hasattr(AerSimulator, "run"):
            original = AerSimulator.run
            _qiskit_originals[(AerSimulator, "run")] = original

            def _aer_run_hook(self, circuits, *args, **kwargs):
                captured = _capture_qiskit_from(circuits, "aer.run")
                _maybe_stop_after_hook()
                return _FakeQiskitJob(captured)

            AerSimulator.run = _aer_run_hook
    except Exception:
        pass

    try:
        from qiskit.quantum_info import Statevector
        raw_from_instruction = Statevector.__dict__.get("from_instruction")
        bound_from_instruction = Statevector.from_instruction
        _qiskit_originals[(Statevector, "from_instruction")] = raw_from_instruction

        def _statevector_from_instruction_hook(cls, instruction, *args, **kwargs):
            _capture_qiskit_from(instruction, "statevector.from_instruction")
            _maybe_stop_after_hook()
            return bound_from_instruction(instruction, *args, **kwargs)

        Statevector.from_instruction = classmethod(_statevector_from_instruction_hook)
    except Exception:
        pass

    try:
        from qiskit.transpiler import PassManager
        if not hasattr(PassManager, "_zxv_orig_run"):
            PassManager._zxv_orig_run = PassManager.run

            def _pm_identity(self, circuits, *args, **kwargs):
                return circuits

            PassManager.run = _pm_identity
            _qiskit_originals[(PassManager, "run")] = PassManager._zxv_orig_run
    except Exception:
        pass

    try:
        from qiskit.transpiler import StagedPassManager
        if not hasattr(StagedPassManager, "_zxv_orig_run"):
            StagedPassManager._zxv_orig_run = StagedPassManager.run

            def _spm_identity(self, circuits, *args, **kwargs):
                return circuits

            StagedPassManager.run = _spm_identity
            _qiskit_originals[(StagedPassManager, "run")] = StagedPassManager._zxv_orig_run
    except Exception:
        pass


def unpatch_qiskit() -> None:
    for (cls, method), orig in _qiskit_originals.items():
        if orig is None:
            try:
                delattr(cls, method)
            except Exception:
                pass
        else:
            setattr(cls, method, orig)
        if hasattr(cls, "_zxv_orig_run"):
            try:
                delattr(cls, "_zxv_orig_run")
            except Exception:
                pass
    _qiskit_originals.clear()


# ---------------------------------------------------------------------------
# Cirq hooks
# ---------------------------------------------------------------------------
_cirq_originals: dict[tuple[type, str], object] = {}


def _make_fake_cirq_result(program, reps: int):
    import cirq
    import numpy as np

    keys: dict[str, int] = {}
    try:
        for op in program.all_operations():
            if cirq.is_measurement(op):
                key = cirq.measurement_key_name(op)
                keys[key] = max(keys.get(key, 0), len(op.qubits))
    except Exception:
        pass
    if not keys:
        keys["m"] = 1
    measurements = {
        k: np.zeros((max(reps, 1), w), dtype=np.int8) for k, w in keys.items()
    }
    try:
        return cirq.ResultDict(
            params=cirq.ParamResolver({}), measurements=measurements
        )
    except Exception:
        return type("FakeResult", (), {"measurements": measurements,
                                        "histogram": lambda **kw: {}})()


def patch_cirq() -> None:
    if _cirq_originals:
        return
    import cirq

    targets = [
        (cirq.Simulator, "run"),
        (cirq.Simulator, "simulate"),
        (cirq.Simulator, "run_sweep"),
        (cirq.DensityMatrixSimulator, "run"),
        (cirq.DensityMatrixSimulator, "simulate"),
    ]
    for cls, method in targets:
        if not hasattr(cls, method):
            continue
        original = getattr(cls, method)
        _cirq_originals[(cls, method)] = original

        def make_hook(orig, mname):
            def hooked(self, program, *args, **kwargs):
                _add_cirq(program, f"cirq.{mname}")
                _maybe_stop_after_hook()
                reps = kwargs.get("repetitions", 1)
                if mname in ("run", "run_sweep"):
                    return _make_fake_cirq_result(program, reps)
                return type("FakeSimRes", (), {"final_state_vector": None,
                                                "measurements": {}})()
            return hooked

        setattr(cls, method, make_hook(original, method))


def unpatch_cirq() -> None:
    for (cls, method), orig in _cirq_originals.items():
        setattr(cls, method, orig)
    _cirq_originals.clear()


# ---------------------------------------------------------------------------
# QPanda3 hooks
# ---------------------------------------------------------------------------
_qpanda3_originals: dict[tuple[type, str], object] = {}


class _FakeQpanda3Result:
    """Minimal QPanda3 result stub used after run() is intercepted."""
    def get_counts(self):
        return {"0" * 4: 1}

    def get_prob_list(self):
        return [1.0]

    def get_prob_dict(self, *a, **kw):
        return {"0": 1.0}


class _FakeQpanda3Job:
    def result(self):
        return _FakeQpanda3Result()

    def get_counts(self):
        return {"0" * 4: 1}

    def get_prob_list(self):
        return [1.0]


def patch_qpanda3() -> None:
    if _qpanda3_originals:
        return

    # 鎷︽埅 CPUQVM.run
    try:
        from pyqpanda3.core import CPUQVM
        if not hasattr(CPUQVM, "_zxv_orig_run"):
            CPUQVM._zxv_orig_run = CPUQVM.run
            original_run = CPUQVM.run
            _qpanda3_originals[(CPUQVM, "run")] = original_run

            def _cpuqvm_run_hook(self, prog, shots=1000, *args, **kwargs):
                _add_qpanda3(prog, "qpanda3.run")
                _maybe_stop_after_hook()
                # 杩斿洖 self 浣?qvm.result() 璋冪敤涔熻兘宸ヤ綔
                self._fake_result = _FakeQpanda3Result()
                return self

            CPUQVM.run = _cpuqvm_run_hook

            # 鍚屾椂 patch result()
            CPUQVM._zxv_orig_result = CPUQVM.result if hasattr(CPUQVM, "result") else None
            def _cpuqvm_result_hook(self):
                if hasattr(self, "_fake_result"):
                    return self._fake_result
                return _FakeQpanda3Result()
            CPUQVM.result = _cpuqvm_result_hook
            _qpanda3_originals[(CPUQVM, "result")] = CPUQVM._zxv_orig_result
    except Exception:
        pass

    # 璁?Transpiler.transpile 鐩存帴杩斿洖鍘熺▼搴忥紙涓嶅仛纭?欢缂栬瘧锛夛紝
    # 淇濈暀鐢ㄦ埛缂栧啓鐨勯棬闆嗗悎锛屾柟渚垮悗缁?簿纭?瘮杈冦€?    try:
        from pyqpanda3.transpilation import Transpiler
        if not hasattr(Transpiler, "_zxv_orig_transpile"):
            Transpiler._zxv_orig_transpile = Transpiler.transpile
            _qpanda3_originals[(Transpiler, "transpile")] = Transpiler._zxv_orig_transpile

            def _transpile_identity(self, prog, *args, **kwargs):
                return prog

            Transpiler.transpile = _transpile_identity
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
# 榛樿?鍙傛暟澶瑰叿
# ---------------------------------------------------------------------------
def _qiskit_oracle():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(4)
    for i in range(3):
        qc.cx(i, 3)
    return qc


def _cirq_oracle():
    import cirq
    qubits = cirq.LineQubit.range(4)
    return cirq.Circuit([cirq.CNOT(qubits[i], qubits[3]) for i in range(3)])


def _qpanda3_oracle():
    from pyqpanda3.core import QCircuit, CNOT
    qc = QCircuit(4)
    for i in range(3):
        qc << CNOT(i, 3)
    return qc


def _vector8():
    return [1.0 / math.sqrt(8.0)] * 8


def _bell_qiskit():
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc


def _bell_cirq():
    import cirq
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1, key="m"))


def _bell_qpanda3():
    from pyqpanda3.core import QCircuit, H, CNOT
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)
    return qc


# 鍑芥暟鍚?-> 榛樿?鍙傛暟瑙勬牸
FUNCTION_ARG_SPECS: dict[str, tuple] = {
    "run_bell_state_simulator": (),
    "bell_each_shot": (),
    "noisy_bell": (),
    "dj_algorithm": ("oracle",),
    "visualize_bell_states": (),
    "sampler_qiskit": (),
    "estimator_qiskit": (),
    "run_multiple_sampler": (),
    "run_jobs_on_batch": (),
    "run_circuit_with_dd_trex": (),
    "init_random_3qubit": ("vector8",),
    "random_coin_flip": (1024,),
    "xor_gate": (85, 51),
    "and_gate": (5, 3),
    "or_gate": (5, 3),
    "not_gate": (170,),
    "zeno_elitzur_vaidman_bomb_tester": (True,),
    "circuit_to_bools": ("bell",),
    "bell_state_noisy": (),
    "run_batched_random_circuits": (),
}


def resolve_args(spec: tuple, framework: str) -> tuple:
    out = []
    for s in spec:
        if s == "oracle":
            if framework == "qiskit":
                out.append(_qiskit_oracle())
            elif framework == "cirq":
                out.append(_cirq_oracle())
            else:
                out.append(_qpanda3_oracle())
        elif s == "vector8":
            if framework == "cirq":
                import numpy as np
                out.append(np.array(_vector8(), dtype=complex))
            else:
                out.append(_vector8())
        elif s == "bell":
            if framework == "qiskit":
                out.append(_bell_qiskit())
            elif framework == "cirq":
                out.append(_bell_cirq())
            else:
                out.append(_bell_qpanda3())
        else:
            out.append(s)
    return tuple(out)


# ---------------------------------------------------------------------------
# 妯″潡鍔犺浇
# ---------------------------------------------------------------------------
def load_module(filepath: str, name: str):
    import io
    import contextlib

    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    devnull = io.StringIO()
    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
        spec.loader.exec_module(mod)
    return mod


def detect_framework(filepath: str) -> str:
    """Infer the framework from import statements."""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return "qiskit"

    has_pennylane = ("import pennylane" in content) or ("from pennylane" in content)
    has_cirq = ("import cirq" in content) or ("from cirq" in content)
    has_qiskit = ("import qiskit" in content) or ("from qiskit" in content)
    has_qpanda3 = ("import pyqpanda3" in content) or ("from pyqpanda3" in content)

    if has_pennylane and not has_cirq and not has_qiskit and not has_qpanda3:
        return "pennylane"
    if has_qpanda3 and not has_cirq and not has_qiskit:
        return "qpanda3"
    if has_cirq and not has_qiskit and not has_qpanda3:
        return "cirq"
    if has_qiskit and not has_cirq and not has_qpanda3:
        return "qiskit"

    # 澶氭?鏋舵贩鐢?細鍙栨渶鍏堝嚭鐜扮殑 import
    positions: dict[str, int] = {}
    if has_qpanda3:
        p = min(
            [p for p in (content.find("import pyqpanda3"), content.find("from pyqpanda3")) if p >= 0],
            default=10**9,
        )
        positions["qpanda3"] = p
    if has_pennylane:
        p = min(
            [p for p in (content.find("import pennylane"), content.find("from pennylane")) if p >= 0],
            default=10**9,
        )
        positions["pennylane"] = p
    if has_cirq:
        p = min(
            [p for p in (content.find("import cirq"), content.find("from cirq")) if p >= 0],
            default=10**9,
        )
        positions["cirq"] = p
    if has_qiskit:
        p = min(
            [p for p in (content.find("import qiskit"), content.find("from qiskit")) if p >= 0],
            default=10**9,
        )
        positions["qiskit"] = p

    if positions:
        return min(positions, key=positions.__getitem__)
    return "qiskit"


def _unique_modname(filepath: str, framework: str) -> str:
    stem = Path(filepath).stem
    return f"{framework}_prog_{stem}"


# ---------------------------------------------------------------------------
# 妗嗘灦鐗瑰畾鐨勭嚎璺?崟鑾峰嚱鏁?# ---------------------------------------------------------------------------
COLLECT_ALL_RUN_TASKS = {28, 53, 54, 55, 56, 68}
MULTI_CIRCUIT_CAPTURE_TASKS = {28}


def _policy_for_idx(idx: int | None) -> dict[str, object]:
    return {
        "stop_after_hook": idx not in COLLECT_ALL_RUN_TASKS,
        "collect_all_circuits": idx in MULTI_CIRCUIT_CAPTURE_TASKS,
    }


def _capture_return_value(ret, framework: str) -> None:
    if framework == "qiskit":
        _capture_qiskit_from(ret, "return_value")
        return
    if framework == "cirq":
        _capture_cirq_from(ret, "return_value")
        return
    if framework == "qpanda3":
        _capture_qpanda3_from(ret, "return_value")
        return
    if framework == "pennylane":
        _capture_pennylane_from(ret, "return_value")
        return
    raise ValueError(f"unsupported framework: {framework}")


def capture_qiskit_generic(filepath: str, fn_name: str, arg_spec: tuple, idx: int | None = None) -> CaptureOutcome:
    _reset_capture(_policy_for_idx(idx))
    patch_qiskit()
    mod_name = _unique_modname(filepath, "qiskit")
    error: str | None = None
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception as exc:
            mod = sys.modules.get(mod_name)
            error = traceback.format_exc() or str(exc)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        should_call_fn = fn is not None and (_collect_all_circuits() or not _captured)
        if should_call_fn:
            try:
                ret = fn(*resolve_args(arg_spec, "qiskit"))
                _capture_return_value(ret, "qiskit")
            except _StoppedExecution:
                pass
            except Exception as exc:
                error = traceback.format_exc() or str(exc)
    finally:
        unpatch_qiskit()
    return CaptureOutcome(list(_captured), list(_capture_sources), error)


def capture_cirq_generic(filepath: str, fn_name: str, arg_spec: tuple, idx: int | None = None) -> CaptureOutcome:
    _reset_capture(_policy_for_idx(idx))
    patch_cirq()
    mod_name = _unique_modname(filepath, "cirq")
    error: str | None = None
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception as exc:
            mod = sys.modules.get(mod_name)
            error = traceback.format_exc() or str(exc)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            try:
                ret = fn(*resolve_args(arg_spec, "cirq"))
                _capture_return_value(ret, "cirq")
            except _StoppedExecution:
                pass
            except Exception as exc:
                error = traceback.format_exc() or str(exc)
    finally:
        unpatch_cirq()
    return CaptureOutcome(list(_captured), list(_capture_sources), error)


def capture_qpanda3_generic(filepath: str, fn_name: str, arg_spec: tuple, idx: int | None = None) -> CaptureOutcome:
    """Capture QPanda3 programs while preserving the original gate sequence."""
    _reset_capture(_policy_for_idx(idx))
    patch_qpanda3()
    mod_name = _unique_modname(filepath, "qpanda3")
    error: str | None = None
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception as exc:
            mod = sys.modules.get(mod_name)
            error = traceback.format_exc() or str(exc)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        if fn is not None and not _captured:
            try:
                ret = fn(*resolve_args(arg_spec, "qpanda3"))
                _capture_return_value(ret, "qpanda3")
            except _StoppedExecution:
                pass
            except Exception as exc:
                error = traceback.format_exc() or str(exc)
    finally:
        unpatch_qpanda3()
    return CaptureOutcome(list(_captured), list(_capture_sources), error)


def capture_pennylane_generic(filepath: str, fn_name: str, arg_spec: tuple, idx: int | None = None) -> CaptureOutcome:
    _reset_capture(_policy_for_idx(idx))
    patch_pennylane()
    mod_name = _unique_modname(filepath, "pennylane")
    error: str | None = None
    try:
        try:
            mod = load_module(filepath, mod_name)
        except _StoppedExecution:
            mod = sys.modules.get(mod_name)
        except Exception as exc:
            mod = sys.modules.get(mod_name)
            error = traceback.format_exc() or str(exc)

        fn = getattr(mod, fn_name, None) if mod is not None else None
        should_call_fn = fn is not None and (_collect_all_circuits() or not _captured)
        if should_call_fn:
            try:
                ret = fn(*resolve_args(arg_spec, "pennylane"))
                _capture_return_value(ret, "pennylane")
            except _StoppedExecution:
                pass
            except Exception as exc:
                error = traceback.format_exc() or str(exc)
    finally:
        unpatch_pennylane()
    return CaptureOutcome(list(_captured), list(_capture_sources), error)


def capture_qiskit(filepath: str, idx: int, prog_dict: dict | None = None) -> CaptureOutcome:
    if prog_dict is not None and idx in prog_dict:
        fn_name, arg_spec = prog_dict[idx][:2]
        return capture_qiskit_generic(filepath, fn_name, arg_spec, idx)
    inferred = _infer_program_entry_from_file(Path(filepath))
    if inferred is None:
        return CaptureOutcome([], [], "entry function not found")
    fn_name, arg_spec = inferred
    return capture_qiskit_generic(filepath, fn_name, arg_spec, idx)


def capture_cirq(filepath: str, idx: int, prog_dict: dict | None = None) -> CaptureOutcome:
    if prog_dict is not None and idx in prog_dict:
        fn_name, arg_spec = prog_dict[idx][:2]
        return capture_cirq_generic(filepath, fn_name, arg_spec, idx)
    inferred = _infer_program_entry_from_file(Path(filepath))
    if inferred is None:
        return CaptureOutcome([], [], "entry function not found")
    fn_name, arg_spec = inferred
    return capture_cirq_generic(filepath, fn_name, arg_spec, idx)


def capture_qpanda3(filepath: str, idx: int, prog_dict: dict | None = None) -> CaptureOutcome:
    if prog_dict is not None and idx in prog_dict:
        fn_name, arg_spec = prog_dict[idx][:2]
        return capture_qpanda3_generic(filepath, fn_name, arg_spec, idx)
    inferred = _infer_program_entry_from_file(Path(filepath))
    if inferred is None:
        return CaptureOutcome([], [], "entry function not found")
    fn_name, arg_spec = inferred
    return capture_qpanda3_generic(filepath, fn_name, arg_spec, idx)


def capture_pennylane(filepath: str, idx: int, prog_dict: dict | None = None) -> CaptureOutcome:
    if prog_dict is not None and idx in prog_dict:
        fn_name, arg_spec = prog_dict[idx][:2]
        return capture_pennylane_generic(filepath, fn_name, arg_spec, idx)
    inferred = _infer_program_entry_from_file(Path(filepath))
    if inferred is None:
        return CaptureOutcome([], [], "entry function not found")
    fn_name, arg_spec = inferred
    return capture_pennylane_generic(filepath, fn_name, arg_spec, idx)


# ---------------------------------------------------------------------------
# 绾胯矾 -> QASM -> pyzx
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
    import numpy as np

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
    """Convert a QPanda3 QProg/QCircuit to measurement-free QASM."""
    from pyqpanda3.intermediate_compiler import convert_qprog_to_qasm
    from pyqpanda3.core import QProg, QCircuit

    # 濡傛灉鎹曡幏鍒扮殑鏄?QCircuit锛岄渶瑕佸厛鍖呰?鎴?QProg
    if isinstance(prog, QCircuit):
        p = QProg()
        p << prog
        prog = p

    try:
        qasm_raw = convert_qprog_to_qasm(prog)
    except Exception as e:
        raise RuntimeError(f"QPanda3 -> QASM failed: {e}") from e

    # 鍓ラ櫎娴嬮噺琛屽拰 creg 澹版槑锛坧yzx 浼氭妸 creg 璇?В涓洪噺瀛愭瘮鐗圭嚎璺?級锛?    # 鍙?繚鐣欓厜鎿嶄綔锛屼緵 pyzx 鍋?ZX 绛変环鎬ф瘮杈冦€?    lines = qasm_raw.splitlines()
    filtered = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("measure"):
            continue
        if stripped.startswith("creg"):
            continue
        filtered.append(line)

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
    filtered = []
    for line in str(qasm_raw).splitlines():
        stripped = line.strip()
        if stripped.startswith("measure") or stripped.startswith("creg"):
            continue
        filtered.append(line)
    return "\n".join(filtered)


def zx_equivalent(qasm_a: str, qasm_b: str) -> tuple[bool | None, str]:
    import pyzx as zx

    try:
        ca = zx.Circuit.from_qasm(qasm_a)
        cb = zx.Circuit.from_qasm(qasm_b)
    except Exception as e:
        return None, f"qasm parse failed: {e}"

    if ca.qubits != cb.qubits:
        return False, f"qubit count mismatch {ca.qubits} vs {cb.qubits}"

    try:
        eq = ca.verify_equality(cb, up_to_global_phase=True)
        return bool(eq), ""
    except Exception as e:
        return None, f"verify_equality failed: {e}"


# ---------------------------------------------------------------------------
# 鎹曡幏缁撴灉姣旇緝锛堟敮鎸佷笁绉嶆?鏋讹級
# ---------------------------------------------------------------------------
def _case_suffix(case_label: str | None) -> str:
    return f"; case={case_label}" if case_label else ""


def _note_no_capture(side: str, fn_name: str | None, case_label: str | None) -> str:
    return (
        f"{side}: no comparable circuit captured; fn={fn_name or ''}"
        f"{_case_suffix(case_label)}"
    )


def _qasm_from_captured(item: tuple[str, object]) -> str:
    fw, circ = item
    if fw == "qiskit":
        return qiskit_to_qasm(circ)
    if fw == "cirq":
        return cirq_to_qasm(circ)
    if fw == "qpanda3":
        return qpanda3_to_qasm(circ)
    if fw == "pennylane":
        return pennylane_to_qasm(circ)
    raise ValueError(f"unknown framework: {fw}")


def _compare_captured(
    circs_a: list,
    circs_b: list,
    case_label: str | None = None,
) -> tuple[str, str]:
    if len(circs_a) != len(circs_b):
        return (
            "NOT_PROVED",
            f"not proved: circuit count mismatch: A captured {len(circs_a)}, "
            f"B captured {len(circs_b)}{_case_suffix(case_label)}",
        )

    flags: list[bool] = []
    notes: list[str] = []

    for i, (item_a, item_b) in enumerate(zip(circs_a, circs_b)):
        try:
            qasm_a = _qasm_from_captured(item_a)
        except Exception as exc:
            return (
                "NOT_PROVED",
                f"not proved: A qasm conversion failed: {exc}{_case_suffix(case_label)}",
            )

        try:
            qasm_b = _qasm_from_captured(item_b)
        except Exception as exc:
            return (
                "NOT_PROVED",
                f"not proved: B qasm conversion failed: {exc}{_case_suffix(case_label)}",
            )

        eq, err = zx_equivalent(qasm_a, qasm_b)
        if eq is None:
            return (
                "NOT_PROVED",
                f"not proved: {err or 'unknown error'}{_case_suffix(case_label)}",
            )
        flags.append(bool(eq))
        if err:
            notes.append(f"#{i}: {err}")

    if flags and all(flags):
        status = "EQUIVALENT"
    elif flags:
        status = "NOT_PROVED"
    else:
        status = "NOT_PROVED"

    detail = (
        f"catch a_circs={len(circs_a)} b_circs={len(circs_b)}"
        + (f" | {' ; '.join(notes)}" if notes else "")
        + _case_suffix(case_label)
    )
    return status, detail


# ---------------------------------------------------------------------------
# Generic pair runner.
# ---------------------------------------------------------------------------
def _capture_by_framework(
    framework: str, filepath: str, idx: int, prog_dict: dict | None = None
) -> CaptureOutcome:
    if framework == "qiskit":
        return capture_qiskit(filepath, idx, prog_dict)
    if framework == "cirq":
        return capture_cirq(filepath, idx, prog_dict)
    if framework == "qpanda3":
        return capture_qpanda3(filepath, idx, prog_dict)
    if framework == "pennylane":
        return capture_pennylane(filepath, idx, prog_dict)
    raise ValueError(f"unsupported framework: {framework}")


def _program_entry(prog: dict | None, idx: int) -> tuple[str | None, tuple, str | None]:
    if not prog or idx not in prog:
        return None, tuple(), None
    entry = prog[idx]
    if len(entry) >= 3:
        return entry[0], tuple(entry[1]), entry[2]
    return entry[0], tuple(entry[1]), None


def _format_sources(outcome_a: CaptureOutcome | None, outcome_b: CaptureOutcome | None) -> str:
    left = ",".join(outcome_a.sources) if outcome_a and outcome_a.sources else ""
    right = ",".join(outcome_b.sources) if outcome_b and outcome_b.sources else ""
    return f"A:{left}; B:{right}"


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

    fn_a, _args_a, case_a = _program_entry(prog_a, idx)
    fn_b, _args_b, case_b = _program_entry(prog_b, idx)
    case_label = case_a or case_b

    out = {"idx": idx, "case": case_label or "", "status": "NOT_PROVED", "detail": "", "capture_source": ""}

    if idx not in prog_a:
        out["detail"] = _note_no_capture("A", fn_a, case_label)
        return out
    if idx not in prog_b:
        out["detail"] = _note_no_capture("B", fn_b, case_label)
        return out

    fw_a = framework_a or detect_framework(file_a)
    fw_b = framework_b or detect_framework(file_b)

    outcome_a: CaptureOutcome | None = None
    outcome_b: CaptureOutcome | None = None
    try:
        outcome_a = _capture_by_framework(fw_a, file_a, idx, prog_a)
    except Exception as exc:
        out["detail"] = f"A: {traceback.format_exc() or str(exc)}"
        return out

    try:
        outcome_b = _capture_by_framework(fw_b, file_b, idx, prog_b)
    except Exception as exc:
        out["capture_source"] = _format_sources(outcome_a, outcome_b)
        out["detail"] = f"B: {traceback.format_exc() or str(exc)}"
        return out

    out["capture_source"] = _format_sources(outcome_a, outcome_b)

    if not outcome_a.circuits:
        out["detail"] = outcome_a.error or _note_no_capture("A", fn_a, case_label)
        return out
    if not outcome_b.circuits:
        out["detail"] = outcome_b.error or _note_no_capture("B", fn_b, case_label)
        return out

    out["status"], out["detail"] = _compare_captured(
        outcome_a.circuits,
        outcome_b.circuits,
        case_label,
    )
    return out

def run_pair(idx: int, file_a: str, file_b: str) -> dict:
    return run_pair_flexible(idx, file_a, file_b)


# ---------------------------------------------------------------------------
# 鍏ュ彛鍑芥暟鎺ㄦ柇
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
            end = int(b.strip())
            step = 1 if end >= start else -1
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
        raise ValueError("pattern must contain '{idx}'")
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


def _discover_paired_indices(dir_a: Path, pattern_a: str, dir_b: Path, pattern_b: str) -> list[int]:
    a_indices = _discover_indices_from_dir(dir_a, pattern_a)
    b_indices = _discover_indices_from_dir(dir_b, pattern_b)
    return sorted(a_indices & b_indices)


def _infer_program_entry_from_file(filepath: Path) -> tuple[str, tuple] | None:
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
        if name in FUNCTION_ARG_SPECS:
            return name, FUNCTION_ARG_SPECS[name]

    # 鍚庡?锛氶€夊彇绗?竴涓?潪绉佹湁鐨勯《灞傚嚱鏁帮紝绌哄弬鏁板垪琛ㄨ瘯璺?    for name in defs_in_order:
        if not name.startswith("_"):
            return name, ()
    return None


def _resolve_program_entry(filepath: Path) -> tuple[tuple[str, tuple] | None, str]:
    inferred = _infer_program_entry_from_file(filepath)
    if inferred is not None:
        fn, _spec = inferred
        return inferred, f"鍑芥暟 `{fn}`"
    return None, "鏂囦欢涓?湭鎵惧埌宸茬煡 Type-A 鍏ュ彛鍑芥暟"


def _resolve_path(base: Path, path_like: str) -> Path:
    p = Path(path_like)
    if not p.is_absolute():
        p = base / p
    return p


# ---------------------------------------------------------------------------
# Status text mapping (English report)
# ---------------------------------------------------------------------------
STATUS_EN = {
    "EQUIVALENT": "Equivalent",
    "NOT_PROVED": "Not Proved",
    "ERROR": "Error",
    "CAPTURE_FAIL": "Capture Failed",
    "MISSING": "File Missing",
    "MIXED": "Mixed Results",
    "UNSUPPORTED": "Unsupported",
    "PENDING": "Pending",
    "CAPTURE_COUNT_MISMATCH": "Circuit Count Mismatch",
}


# ---------------------------------------------------------------------------
# 涓荤▼搴?# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None):
    from zx_unified import legacy_main
    return legacy_main("type1", globals(), argv)

if __name__ == "__main__":
    main()

