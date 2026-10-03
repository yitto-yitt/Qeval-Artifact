# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    def _as_list(x):
        try:
            return list(x)
        except Exception:
            return None

    def _qubit_addr(q):
        for name in ("get_phy_addr", "getPhysicalQubitPtr", "get_phy_addr_"):
            try:
                return int(getattr(q, name)())
            except Exception:
                pass
        return 0

    source = oracle
    oracle_obj = oracle
    qubits = None
    n = None

    if isinstance(oracle, dict):
        for k in ("oracle", "circuit", "prog", "program"):
            if k in oracle:
                oracle_obj = oracle[k]
                break
        for k in ("qubits", "qvec", "qv", "q"):
            if k in oracle:
                qubits = _as_list(oracle[k])
                break
        for k in ("num_qubits", "n"):
            if k in oracle:
                n = int(oracle[k])
                break

    elif isinstance(oracle, (tuple, list)):
        for item in oracle:
            lst = _as_list(item)
            if lst is not None and len(lst) > 0 and hasattr(lst[0], "get_phy_addr"):
                qubits = lst
            elif hasattr(item, "get_used_qubits") or hasattr(item, "get_used_cbits"):
                oracle_obj = item
            elif isinstance(item, int):
                n = int(item)
        source = oracle_obj

    if n is None:
        try:
            n = int(getattr(source, "num_qubits"))
        except Exception:
            try:
                n = int(source.num_qubits())
            except Exception:
                pass

    if qubits is None:
        for attr in ("qubits", "qvec", "qv", "q"):
            try:
                candidate = getattr(source, attr)
                if callable(candidate):
                    candidate = candidate()
                candidate = _as_list(candidate)
                if candidate is not None and len(candidate) > 0:
                    qubits = candidate
                    break
            except Exception:
                pass

    if qubits is None:
        try:
            used = source.get_used_qubits()
            qubits = sorted(list(used), key=_qubit_addr)
        except Exception:
            try:
                used = QVec()
                source.get_used_qubits(used)
                qubits = sorted(list(used), key=_qubit_addr)
            except Exception:
                qubits = None

    if n is None and qubits is not None:
        n = len(qubits)

    if qubits is None or (n is not None and len(qubits) < n):
        try:
            qubits = qAlloc_many(int(n))
        except Exception:
            try:
                init(QMachineType.CPU)
            except Exception:
                pass
            qubits = qAlloc_many(int(n))

    n = int(n)

    if callable(oracle_obj) and not hasattr(oracle_obj, "get_used_qubits"):
        result = oracle_obj(qubits)
        if result is not None:
            oracle_obj = result

    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle_obj
    for i in range(n):
        prog << H(qubits[i])

    input_qubits = [qubits[i] for i in range(n - 1)]
    if len(input_qubits) == 0:
        return {"": 1.0}

    measure_qubits = input_qubits
    if len(input_qubits) > 1:
        try:
            cal_q = qAlloc_many(2)
            cal_prog = QProg()
            cal_prog << X(cal_q[0])
            cal_probs = prob_run_dict(cal_prog, cal_q, -1)
            top_key = max(cal_probs, key=cal_probs.get)
            if str(top_key)[0] == "1":
                measure_qubits = list(reversed(input_qubits))
        except Exception:
            measure_qubits = list(reversed(input_qubits))

    try:
        probs = prob_run_dict(prog, measure_qubits, -1)
        result = {}
        for key, value in probs.items():
            value = float(value)
            if value > 1e-12:
                result[str(key)] = value
        total = builtins.sum(result.values())
        if total != 0:
            return {key: value / total for key, value in result.items()}
        return result
    except Exception:
        cbits = cAlloc_many(n - 1)
        meas_prog = QProg()
        meas_prog << prog
        for i in range(n - 1):
            meas_prog << Measure(qubits[i], cbits[i])
        shots = 1024
        counts = run_with_configuration(meas_prog, cbits, shots)
        total = builtins.sum(counts.values())
        return {str(key): value / total for key, value in counts.items()}
