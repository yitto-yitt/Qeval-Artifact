# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    def _call_if_exists(obj, names):
        for name in names:
            method = getattr(obj, name, None)
            if method is not None:
                try:
                    method()
                    return
                except TypeError:
                    pass

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "alloc_qubits"):
            method = getattr(machine, name, None)
            if method is not None:
                try:
                    qv = method(n)
                    return [qv[i] for i in range(n)]
                except Exception:
                    pass
        for name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            method = getattr(machine, name, None)
            if method is not None:
                return [method() for _ in range(n)]
        raise RuntimeError("No compatible qubit allocation API found")

    def _append_ccx(prog, c1, c2, target):
        for name in ("Toffoli", "TOFFOLI", "CCX", "CCNOT"):
            factory = globals().get(name)
            if factory is not None:
                try:
                    prog << factory(c1, c2, target)
                    return
                except Exception:
                    pass
        gate = X(target)
        for name in ("control", "set_control", "setControl"):
            method = getattr(gate, name, None)
            if method is not None:
                try:
                    prog << method([c1, c2])
                    return
                except Exception:
                    pass
        raise RuntimeError("No compatible controlled-controlled-X gate API found")

    def _prob_run(machine, prog, qlist):
        for name in ("prob_run_dict", "prob_run_tuple_list", "prob_run_list"):
            method = getattr(machine, name, None)
            if method is not None:
                for args in ((prog, qlist, -1), (prog, qlist), (prog, qlist, 2)):
                    try:
                        return method(*args)
                    except Exception:
                        pass
        raise RuntimeError("No compatible probability run API found")

    def _p1_from_result(result):
        if isinstance(result, dict):
            total = 0.0
            one = 0.0
            for key, value in result.items():
                try:
                    p = float(value.real if hasattr(value, "real") else value)
                except Exception:
                    p = float(value)
                if p < 0:
                    p = 0.0
                if isinstance(key, int):
                    bit = key & 1
                else:
                    s = str(key)
                    bits = "".join(ch for ch in s if ch in "01")
                    bit = 1 if bits and bits[-1] == "1" else 0
                total += p
                if bit:
                    one += p
            return one / total if total else 0.0
        if isinstance(result, (list, tuple)):
            if len(result) > 0 and isinstance(result[0], (list, tuple)) and len(result[0]) == 2:
                return _p1_from_result(dict(result))
            vals = [float(v.real if hasattr(v, "real") else v) for v in result]
            total = sum(vals)
            return (vals[1] / total) if total and len(vals) > 1 else 0.0
        return 0.0

    machine = CPUQVM()
    _call_if_exists(machine, ("init_qvm", "init"))
    try:
        qubits = _alloc_qubits(machine, 9)
        prog = QProg()

        a_bits = format(int(a), "03b")
        b_bits = format(int(b), "03b")

        for i in range(3):
            if a_bits[2 - i] == "1":
                prog << X(qubits[i])
            if b_bits[2 - i] == "1":
                prog << X(qubits[3 + i])

        for i in range(3):
            _append_ccx(prog, qubits[i], qubits[3 + i], qubits[6 + i])

        out = []
        for idx in (8, 7, 6):
            p1 = _p1_from_result(_prob_run(machine, prog, [qubits[idx]]))
            out.append("1" if p1 > 0.5 else "0")

        return {"".join(out): 1.0}
    finally:
        _call_if_exists(machine, ("finalize", "finalize_qvm"))
