# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *

def xor_gate(a, b):
    shots = 1024

    def _call_first(obj, names, *args):
        last_exc = None
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args)
                except Exception as exc:
                    last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise AttributeError(names[0])

    def _normalize_key(key):
        if isinstance(key, int):
            bits = bin(key)[2:]
        else:
            s = str(key).strip().replace(" ", "")
            if s.startswith(("0b", "0B")):
                s = s[2:]
            bits = "".join(ch for ch in s if ch in "01")
        if len(bits) < 8:
            bits = bits.zfill(8)
        elif len(bits) > 8:
            bits = bits[-8:]
        return bits

    def _to_probs(data):
        accum = {}
        for k, v in dict(data).items():
            val = float(v)
            if val > 1e-12:
                key = _normalize_key(k)
                accum[key] = accum.get(key, 0.0) + val
        total = sum(accum.values())
        return {k: v / total for k, v in accum.items()} if total else {}

    qvm = CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except Exception:
                pass

    qraw = _call_first(qvm, ("qAlloc_many", "qalloc_many", "qallocMany"), 8)
    qubits = [qraw[i] for i in range(8)]

    prog = QProg()

    def _append(node):
        nonlocal prog
        try:
            new_prog = prog << node
            if new_prog is not None:
                prog = new_prog
        except Exception:
            new_prog = prog.insert(node)
            if new_prog is not None:
                prog = new_prog

    a = int(a)
    b = int(b)

    for i in range(8):
        if (a >> i) & 1:
            _append(X(qubits[i]))
    for i in range(8):
        if (b >> i) & 1:
            _append(X(qubits[i]))

    q_order_list = [qubits[i] for i in range(7, -1, -1)]
    q_orders = [q_order_list]
    if "QVec" in globals():
        try:
            qv = QVec()
            for q in q_order_list:
                try:
                    qv.append(q)
                except Exception:
                    qv.push_back(q)
            q_orders.append(qv)
        except Exception:
            pass

    try:
        if hasattr(qvm, "prob_run_dict"):
            for q_order in q_orders:
                try:
                    result = qvm.prob_run_dict(prog, q_order, -1)
                    probs = _to_probs(result)
                    if probs:
                        if hasattr(qvm, "finalize"):
                            try:
                                qvm.finalize()
                            except Exception:
                                pass
                        return probs
                except Exception:
                    try:
                        result = qvm.prob_run_dict(prog, q_order)
                        probs = _to_probs(result)
                        if probs:
                            if hasattr(qvm, "finalize"):
                                try:
                                    qvm.finalize()
                                except Exception:
                                    pass
                            return probs
                    except Exception:
                        pass
    except Exception:
        pass

    try:
        if hasattr(qvm, "directly_run"):
            qvm.directly_run(prog)
            qm = getattr(qvm, "quick_measure", None)
            if qm is None and "quick_measure" in globals():
                qm = globals()["quick_measure"]
            if qm is not None:
                for q_order in q_orders:
                    try:
                        counts = qm(q_order, shots)
                        probs = _to_probs(counts)
                        if probs:
                            if hasattr(qvm, "finalize"):
                                try:
                                    qvm.finalize()
                                except Exception:
                                    pass
                            return probs
                    except Exception:
                        pass
    except Exception:
        pass

    craw = _call_first(qvm, ("cAlloc_many", "calloc_many", "cAllocMany"), 8)
    cbits = [craw[i] for i in range(8)]

    if "Measure" in globals():
        for i in range(8):
            _append(Measure(qubits[7 - i], cbits[i]))
    elif "measure" in globals():
        for i in range(8):
            _append(measure(qubits[7 - i], cbits[i]))
    else:
        _append(measure_all(q_order_list, cbits))

    counts = None
    for c_arg in (craw, cbits):
        try:
            counts = qvm.run_with_configuration(prog, c_arg, shots)
            break
        except Exception:
            try:
                counts = qvm.run_with_configuration(prog, shots, c_arg)
                break
            except Exception:
                pass

    probs = _to_probs(counts)
    if hasattr(qvm, "finalize"):
        try:
            qvm.finalize()
        except Exception:
            pass
    return probs
