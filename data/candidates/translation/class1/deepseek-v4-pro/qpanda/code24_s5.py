# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    q = None
    for attr in ("get_used_qubits", "get_qubits", "qubits"):
        if hasattr(oracle, attr):
            try:
                val = getattr(oracle, attr)
                if callable(val):
                    val = val()
                qlist = list(val)
                if qlist:
                    q = qlist
                    break
            except Exception:
                continue

    if q is None:
        if hasattr(oracle, "num_qubits"):
            n = oracle.num_qubits
            q = qAlloc_many(n)
        else:
            raise ValueError("Cannot determine oracle qubit count")

    n = len(q)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])

    try:
        return prob_run_dict(prog, q[:n - 1])
    except NameError:
        c = cAlloc_many(n - 1)
        for i in range(n - 1):
            prog << measure(q[i], c[i])
        counts = run_with_configuration(prog, c, 10000)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
