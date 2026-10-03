# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *


def dj_algorithm(oracle):
    def _call(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                attr = getattr(obj, name)
                if callable(attr):
                    try:
                        return attr(*args)
                    except TypeError:
                        try:
                            return attr()
                        except TypeError:
                            pass
                else:
                    return attr
        return None

    def _as_list(x):
        if x is None:
            return None
        try:
            return list(x)
        except TypeError:
            return None

    def _num_qubits(obj):
        n = _call(obj, ["num_qubits", "qubit_count", "get_qubit_num", "get_qubits_num", "get_qgate_num"])
        if callable(n):
            n = n()
        if n is not None:
            try:
                return int(n)
            except Exception:
                pass
        qs = _qubits(obj)
        if qs is not None:
            return len(qs)
        raise ValueError("Cannot determine oracle qubit count")

    def _qubits(obj):
        for names in (
            ["qubits", "qbits", "qvec", "qv"],
            ["get_used_qubits", "get_used_qbits", "get_qubits", "get_qbits", "get_qvec"],
        ):
            qs = _as_list(_call(obj, names))
            if qs is not None:
                return qs
        for fn_name in ("get_used_qubits", "get_used_qbits", "get_all_used_qubits"):
            fn = globals().get(fn_name)
            if callable(fn):
                try:
                    qs = _as_list(fn(obj))
                    if qs is not None:
                        return qs
                except Exception:
                    pass
        return None

    def _init_machine():
        m = CPUQVM()
        for name in ("init_qvm", "init", "initQVM"):
            if hasattr(m, name):
                try:
                    getattr(m, name)()
                    break
                except Exception:
                    pass
        return m

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qalloc_many"):
            if hasattr(machine, name):
                return list(getattr(machine, name)(n))
        return [machine.qAlloc() for _ in range(n)]

    def _probabilities(machine, prog, qlist):
        attempts = (
            ("prob_run_dict", (prog, qlist, -1)),
            ("prob_run_dict", (prog, qlist)),
            ("get_prob_dict", (prog, qlist)),
            ("pmeasure", (prog, qlist)),
            ("PMeasure", (prog, qlist)),
        )
        for name, args in attempts:
            if hasattr(machine, name):
                try:
                    return dict(getattr(machine, name)(*args))
                except Exception:
                    pass
        fn = globals().get("prob_run_dict")
        if callable(fn):
            try:
                return dict(fn(prog, qlist, -1))
            except Exception:
                pass
        raise RuntimeError("No probability execution method available")

    n = _num_qubits(oracle)
    machine = _init_machine()
    qubits = _qubits(oracle)
    if qubits is None or len(qubits) < n:
        qubits = _alloc_qubits(machine, n)

    prog = QProg()
    prog << X(qubits[n - 1])
    for q in qubits[:n]:
        prog << H(q)
    prog << oracle
    for q in qubits[:n]:
        prog << H(q)

    input_qubits = list(reversed(qubits[: n - 1]))
    probs = _probabilities(machine, prog, input_qubits)

    result = {}
    for key, value in probs.items():
        if isinstance(key, (list, tuple)):
            bitstr = "".join(str(int(b)) for b in key)
        else:
            bitstr = str(key)
        try:
            p = float(value)
        except Exception:
            p = float(value.real)
        if p > 1e-12:
            result[bitstr] = p

    total = sum(result.values())
    if total != 0:
        result = {k: v / total for k, v in result.items()}
    return result
