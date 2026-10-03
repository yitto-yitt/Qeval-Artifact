# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *

def visualize_bell_states():
    shots = 1000

    def _init_machine():
        machine = pq.CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, name):
                method = getattr(machine, name)
                if callable(method):
                    try:
                        method()
                    except TypeError:
                        pass
                    break
        return machine

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        return [machine.qAlloc() for _ in range(n)]

    def _alloc_cbits(machine, n):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        return [machine.cAlloc() for _ in range(n)]

    def _normalize_key(key):
        if isinstance(key, int):
            return format(key, "02b")
        if isinstance(key, bytes):
            key = key.decode()
        s = str(key).strip()
        if s.startswith("0x"):
            try:
                return format(int(s, 16), "02b")
            except ValueError:
                pass
        bits = "".join(ch for ch in s if ch in "01")
        if len(bits) >= 2:
            return bits[-2:]
        return s

    def _to_probabilities(result):
        if hasattr(result, "get_counts") and callable(result.get_counts):
            result = result.get_counts()
        elif hasattr(result, "to_dict") and callable(result.to_dict):
            result = result.to_dict()

        if isinstance(result, dict):
            data = result
        else:
            try:
                data = dict(result)
            except Exception:
                data = {}

        cleaned = {}
        for key, value in data.items():
            try:
                val = float(value)
            except Exception:
                continue
            if val > 0:
                cleaned[_normalize_key(key)] = cleaned.get(_normalize_key(key), 0.0) + val

        total = sum(cleaned.values())
        if total == 0:
            return {}
        return {key: value / total for key, value in cleaned.items()}

    def _build_program(qubits, cbits, minus=False, with_measure=True):
        prog = pq.QProg()
        if minus:
            prog << pq.X(qubits[0])
        prog << pq.H(qubits[0])
        prog << pq.CNOT(qubits[0], qubits[1])
        if with_measure:
            measured = False
            if hasattr(pq, "measure_all"):
                try:
                    prog << pq.measure_all(qubits, cbits)
                    measured = True
                except Exception:
                    measured = False
            if not measured and hasattr(pq, "MeasureAll"):
                try:
                    prog << pq.MeasureAll(qubits, cbits)
                    measured = True
                except Exception:
                    measured = False
            if not measured:
                for i in range(2):
                    prog << pq.Measure(qubits[i], cbits[i])
        return prog

    def _run_bell(minus=False):
        machine = _init_machine()
        qubits = _alloc_qubits(machine, 2)
        cbits = _alloc_cbits(machine, 2)
        prog = _build_program(qubits, cbits, minus=minus, with_measure=True)

        if hasattr(machine, "run_with_configuration"):
            runner = getattr(machine, "run_with_configuration")
            for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                try:
                    probs = _to_probabilities(runner(*args))
                    if probs:
                        return probs
                except Exception:
                    pass

        for name in ("run", "run_with_shots", "sample"):
            if hasattr(machine, name):
                runner = getattr(machine, name)
                for args in ((prog, cbits, shots), (prog, shots, cbits), (prog, shots)):
                    try:
                        probs = _to_probabilities(runner(*args))
                        if probs:
                            return probs
                    except Exception:
                        pass

        prog = _build_program(qubits, cbits, minus=minus, with_measure=False)
        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            if hasattr(machine, name):
                runner = getattr(machine, name)
                for args in ((prog, qubits, -1), (prog, qubits), (prog,)):
                    try:
                        result = runner(*args)
                        if isinstance(result, (list, tuple)):
                            result = {i: v for i, v in enumerate(result)}
                        probs = _to_probabilities(result)
                        if probs:
                            return probs
                    except Exception:
                        pass

        raise RuntimeError("Unable to execute pyQPanda3 quantum program")

    return {
        "phi_plus": _run_bell(False),
        "phi_minus": _run_bell(True),
    }
