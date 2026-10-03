# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    def _call_if(obj, name, *args):
        attr = getattr(obj, name, None)
        if attr is None:
            return None
        try:
            return attr(*args) if callable(attr) else attr
        except TypeError:
            return None

    def _as_list(x):
        if x is None:
            return None
        try:
            return list(x)
        except TypeError:
            return None

    def _addr(q):
        for name in ("get_phy_addr", "getPhysicalQubitPtr", "get_phy_addr_"):
            attr = getattr(q, name, None)
            if attr is not None:
                try:
                    return int(attr() if callable(attr) else attr)
                except Exception:
                    pass
        for name in ("phy_addr", "physical_addr", "addr", "id", "index"):
            attr = getattr(q, name, None)
            if attr is not None:
                try:
                    return int(attr() if not callable(attr) else attr())
                except Exception:
                    pass
        return 0

    qvm = None
    for name in ("qvm", "machine", "vm"):
        qvm = getattr(oracle, name, None)
        if qvm is not None:
            break
    if qvm is None:
        qvm = CPUQVM()
        for init_name in ("init_qvm", "init"):
            init = getattr(qvm, init_name, None)
            if init is not None:
                try:
                    init()
                except TypeError:
                    pass
                break

    qubits = None
    for name in ("qubits", "qlist", "qvec", "q"):
        qubits = _as_list(getattr(oracle, name, None))
        if qubits:
            break
    if not qubits:
        for name in ("get_used_qubits", "get_all_used_qubits", "get_used_qbits", "used_qubits"):
            qubits = _as_list(_call_if(oracle, name))
            if qubits:
                break
    if not qubits and "get_all_used_qubits" in globals():
        try:
            qubits = list(get_all_used_qubits(oracle))
        except Exception:
            qubits = None

    n = None
    for name in ("num_qubits", "qubit_num", "n_qubits", "num"):
        attr = getattr(oracle, name, None)
        if attr is not None:
            try:
                n = int(attr() if callable(attr) else attr)
                break
            except Exception:
                pass

    oracle_circuit = oracle
    if qubits is None:
        if n is None:
            raise ValueError("Cannot determine oracle qubits")
        qubits = list(qvm.qAlloc_many(n))
        if callable(oracle):
            oracle_circuit = oracle(qubits)
    else:
        qubits = sorted(qubits, key=_addr)
        if n is None:
            n = len(qubits)
        qubits = qubits[:n]

    prog = QProg()
    prog << X(qubits[n - 1])
    for q in qubits:
        prog << H(q)
    prog << oracle_circuit
    for q in qubits:
        prog << H(q)

    input_qubits = list(reversed(qubits[:n - 1]))
    if len(input_qubits) == 0:
        return {"": 1.0}

    result = None
    for args in (
        (prog, input_qubits, -1),
        (prog, input_qubits),
    ):
        try:
            result = qvm.prob_run_dict(*args)
            break
        except Exception:
            result = None

    if result is None:
        for name in ("get_prob_dict", "prob_run"):
            method = getattr(qvm, name, None)
            if method is not None:
                try:
                    result = method(prog, input_qubits)
                    break
                except Exception:
                    pass

    if result is None:
        prob_list = None
        for args in (
            (prog, input_qubits, -1),
            (prog, input_qubits),
        ):
            try:
                prob_list = qvm.prob_run_list(*args)
                break
            except Exception:
                prob_list = None
        if prob_list is not None:
            width = len(input_qubits)
            result = {format(i, "0{}b".format(width)): float(p) for i, p in enumerate(prob_list)}

    if result is None:
        cbits = list(qvm.cAlloc_many(n - 1))
        meas_prog = QProg()
        meas_prog << prog
        for i, q in enumerate(qubits[:n - 1]):
            try:
                meas_prog << Measure(q, cbits[i])
            except Exception:
                meas_prog << measure(q, cbits[i])
        counts = None
        for args in (
            (meas_prog, cbits, 8192),
            (meas_prog, 8192, cbits),
        ):
            try:
                counts = qvm.run_with_configuration(*args)
                break
            except Exception:
                counts = None
        if counts is None:
            counts = qvm.run(meas_prog, 8192)
        total = float(sum(counts.values()))
        return {str(k): float(v) / total for k, v in counts.items() if v}

    cleaned = {}
    for k, v in dict(result).items():
        p = float(v)
        if p > 1e-12:
            key = str(k)
            if len(key) != n - 1:
                try:
                    key = format(int(key), "0{}b".format(n - 1))
                except Exception:
                    key = key.zfill(n - 1)
            cleaned[key] = cleaned.get(key, 0.0) + p

    total = sum(cleaned.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in cleaned.items()}
