# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *


def xor_gate(a, b):
    def _init_machine(m):
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    return
                except TypeError:
                    pass

    def _alloc_qubits(m, n):
        for name in ("qAlloc_many", "qalloc_many", "qallocMany", "allocate_qubits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        raise AttributeError("No qubit allocation method found")

    def _alloc_cbits(m, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
            if hasattr(m, name):
                return getattr(m, name)(n)
        raise AttributeError("No cbit allocation method found")

    def _normalize_result(raw):
        out = {}
        for k, v in dict(raw).items():
            if isinstance(k, int):
                key = format(k, "08b")
            else:
                key = "".join(ch for ch in str(k) if ch in "01")
                if len(key) < 8:
                    key = key.zfill(8)
                elif len(key) > 8:
                    key = key[-8:]
            val = float(v.real if hasattr(v, "real") else v)
            if val > 1e-12:
                out[key] = out.get(key, 0.0) + val
        total = sum(out.values())
        if total == 0:
            return out
        return {k: v / total for k, v in out.items()}

    machine = pq.CPUQVM()
    _init_machine(machine)

    qubits = _alloc_qubits(machine, 8)
    prog = pq.QProg()

    for i in range(8):
        if (int(a) >> i) & 1:
            prog << pq.X(qubits[i])
    for i in range(8):
        if (int(b) >> i) & 1:
            prog << pq.X(qubits[i])

    measure_qubits = [qubits[i] for i in range(7, -1, -1)]

    for args in (
        (prog, measure_qubits, -1),
        (prog, measure_qubits),
    ):
        if hasattr(machine, "prob_run_dict"):
            try:
                return _normalize_result(machine.prob_run_dict(*args))
            except Exception:
                pass
        if hasattr(pq, "prob_run_dict"):
            try:
                return _normalize_result(pq.prob_run_dict(*args))
            except Exception:
                pass

    cbits = _alloc_cbits(machine, 8)
    if hasattr(pq, "measure_all"):
        prog << pq.measure_all(measure_qubits, cbits)
    else:
        for i in range(8):
            prog << pq.Measure(measure_qubits[i], cbits[i])

    shots = 1024
    raw = None
    for name in ("run_with_configuration", "runWithConfiguration"):
        if hasattr(machine, name):
            try:
                raw = getattr(machine, name)(prog, cbits, shots)
                break
            except Exception:
                try:
                    raw = getattr(machine, name)(prog, shots)
                    break
                except Exception:
                    pass
    if raw is None:
        for name in ("run", "directly_run"):
            if hasattr(machine, name):
                try:
                    raw = getattr(machine, name)(prog, shots)
                    break
                except Exception:
                    try:
                        raw = getattr(machine, name)(prog)
                        break
                    except Exception:
                        pass

    return _normalize_result(raw)
