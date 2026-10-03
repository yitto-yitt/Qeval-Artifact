# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq
from collections import Counter

def bell_each_shot():
    def _call_first(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)(*args)
        raise AttributeError(names[0])

    def _normalize_result(res):
        if hasattr(res, "get_counts"):
            res = res.get_counts()
        if hasattr(res, "to_dict"):
            try:
                res = res.to_dict()
            except Exception:
                pass
        if isinstance(res, (list, tuple)):
            if all(isinstance(x, str) for x in res):
                res = dict(Counter(res))
            elif len(res) == 1:
                return _normalize_result(res[0])
        if not isinstance(res, dict):
            raise TypeError("Unsupported result type")

        flat = {}
        for k, v in res.items():
            if isinstance(v, dict):
                sub = _normalize_result(v)
                for sk, sv in sub.items():
                    flat[sk] = flat.get(sk, 0.0) + sv
                continue

            if isinstance(k, str):
                key = k.replace(" ", "")
            elif isinstance(k, int):
                key = format(k, "02b")
            elif isinstance(k, (list, tuple)):
                key = "".join(str(int(x)) for x in k)
            else:
                key = str(k).replace(" ", "")

            try:
                val = float(v)
            except Exception:
                continue
            if val > 1e-12:
                flat[key] = flat.get(key, 0.0) + val

        total = sum(flat.values())
        if total <= 0:
            raise ValueError("Empty result")
        return {k: v / total for k, v in flat.items()}

    def _init_qvm(qvm):
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(qvm, name):
                try:
                    getattr(qvm, name)()
                    return
                except TypeError:
                    pass

    def _alloc_qubits(qvm):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(qvm, name):
                return list(getattr(qvm, name)(2))
        for name in ("qAlloc", "qalloc"):
            if hasattr(qvm, name):
                return [getattr(qvm, name)(), getattr(qvm, name)()]
        if hasattr(pq, "Qubit"):
            return [pq.Qubit(0), pq.Qubit(1)]
        return [0, 1]

    def _alloc_cbits(qvm):
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            if hasattr(qvm, name):
                return list(getattr(qvm, name)(2))
        for name in ("cAlloc", "calloc"):
            if hasattr(qvm, name):
                return [getattr(qvm, name)(), getattr(qvm, name)()]
        if hasattr(pq, "CBit"):
            return [pq.CBit(0), pq.CBit(1)]
        return [0, 1]

    def _cnot(a, b):
        for name in ("CNOT", "CX"):
            if hasattr(pq, name):
                return getattr(pq, name)(a, b)
        raise AttributeError("CNOT")

    def _measure(q, c):
        for name in ("Measure", "measure"):
            if hasattr(pq, name):
                return getattr(pq, name)(q, c)
        raise AttributeError("Measure")

    def _build_prog(q, c=None, with_measure=True):
        prog = pq.QProg()
        prog << pq.H(q[0])
        prog << _cnot(q[0], q[1])
        if with_measure:
            if c is None:
                c = [0, 1]
            if hasattr(pq, "measure_all"):
                try:
                    prog << pq.measure_all(q, c)
                    return prog
                except Exception:
                    pass
            prog << _measure(q[0], c[0])
            prog << _measure(q[1], c[1])
        return prog

    qvm = pq.CPUQVM()
    _init_qvm(qvm)
    qubits = _alloc_qubits(qvm)
    cbits = _alloc_cbits(qvm)

    prog = _build_prog(qubits, cbits, True)

    run_attempts = [
        lambda: qvm.run_with_configuration(prog, cbits, 10),
        lambda: qvm.run_with_configuration(prog, 10),
        lambda: qvm.run(prog, 10),
        lambda: qvm.run(prog, shots=10),
        lambda: qvm.run(prog, cbits, 10),
    ]

    for attempt in run_attempts:
        try:
            return _normalize_result(attempt())
        except Exception:
            pass

    prog_nom = _build_prog(qubits, cbits, False)

    prob_attempts = [
        lambda: qvm.prob_run_dict(prog_nom, qubits, -1),
        lambda: qvm.prob_run_dict(prog_nom, qubits),
    ]

    for attempt in prob_attempts:
        try:
            return _normalize_result(attempt())
        except Exception:
            pass

    if hasattr(qvm, "directly_run"):
        try:
            qvm.directly_run(prog_nom)
            for attempt in (
                lambda: qvm.get_prob_dict(qubits, -1),
                lambda: qvm.get_prob_dict(qubits),
            ):
                try:
                    return _normalize_result(attempt())
                except Exception:
                    pass
        except Exception:
            pass

    raise RuntimeError("Unable to execute Bell circuit with pyQPanda3")
