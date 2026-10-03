# EVAL_META: task_id=68, framework=qpanda, class=1
import math
import pyqpanda3.core as pq

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    angle = math.pi / cycles

    def _init_machine(machine):
        for name in ("init_qvm", "init"):
            if hasattr(machine, name):
                getattr(machine, name)()
                return

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_qubits"):
            if hasattr(machine, name):
                res = getattr(machine, name)(n)
                try:
                    return list(res)
                except TypeError:
                    return res
        for name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise RuntimeError("No qubit allocation method found")

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "allocate_cbits", "alloc_cbits"):
            if hasattr(machine, name):
                res = getattr(machine, name)(n)
                try:
                    return list(res)
                except TypeError:
                    return res
        for name in ("cAlloc", "calloc", "allocate_cbit", "alloc_cbit"):
            if hasattr(machine, name):
                return [getattr(machine, name)() for _ in range(n)]
        raise RuntimeError("No cbit allocation method found")

    def _ry(q, theta):
        for name in ("RY", "ry"):
            if hasattr(pq, name):
                return getattr(pq, name)(q, theta)
        raise RuntimeError("No RY gate found")

    def _measure(q, c):
        for name in ("Measure", "measure", "MEASURE"):
            if hasattr(pq, name):
                return getattr(pq, name)(q, c)
        raise RuntimeError("No measurement operation found")

    def _run_counts(machine, prog, cbits, shots):
        for name in ("run_with_configuration", "run_with_config", "runWithConfiguration"):
            if hasattr(machine, name):
                result = getattr(machine, name)(prog, cbits, shots)
                if hasattr(result, "get_counts"):
                    return result.get_counts()
                if isinstance(result, dict):
                    return result
                return dict(result)
        raise RuntimeError("No shot execution method found")

    def _clean_key(key):
        return "".join(ch for ch in str(key) if ch in "01")

    machine = pq.CPUQVM()
    _init_machine(machine)
    qubits = _alloc_qubits(machine, 1)

    if bomb_live:
        cbits = _alloc_cbits(machine, cycles + 2)
        prog = pq.QProg()
        for i in range(cycles):
            prog << _ry(qubits[0], angle)
            prog << _measure(qubits[0], cbits[i + 1])
        prog << _measure(qubits[0], cbits[0])
        prog << _measure(qubits[0], cbits[cycles + 1])
        counts = _run_counts(machine, prog, cbits, shots)

        live_predictions = 0.0
        dud_predictions = 0.0
        detonations = 0.0

        for key, value in counts.items():
            bitstring = _clean_key(key)
            value = float(value)
            if bitstring and (bitstring[0] == "1" or bitstring[-1] == "1"):
                detonations += value
            elif "1" in bitstring[1:-1]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        cbits = _alloc_cbits(machine, 1)
        prog = pq.QProg()
        for _ in range(cycles):
            prog << _ry(qubits[0], angle)
        prog << _measure(qubits[0], cbits[0])
        counts = _run_counts(machine, prog, cbits, shots)

        live_predictions = 0.0
        dud_predictions = 0.0
        detonations = 0.0

        for key, value in counts.items():
            bitstring = _clean_key(key)
            value = float(value)
            if bitstring and bitstring[-1] == "1":
                dud_predictions += value
            else:
                live_predictions += value

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
