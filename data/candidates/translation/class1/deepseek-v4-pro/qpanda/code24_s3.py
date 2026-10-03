# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import qAlloc_many, QProg, H, X, probRunDict


def dj_algorithm(oracle):
    qubits = None
    for attr in ('getQubits', 'get_qubits', 'getUsedQubits', 'get_used_qubits'):
        if hasattr(oracle, attr):
            try:
                q = getattr(oracle, attr)()
                if q is not None:
                    qubits = list(q)
                    if qubits:
                        break
            except Exception:
                pass

    if qubits is None:
        if hasattr(oracle, 'getQubitNum'):
            n = oracle.getQubitNum()
        elif hasattr(oracle, 'get_qubit_num'):
            n = oracle.get_qubit_num()
        elif hasattr(oracle, 'num_qubits'):
            n = oracle.num_qubits
        else:
            raise ValueError("Cannot determine oracle qubit count")
        qubits = qAlloc_many(n)

    n = len(qubits)

    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])

    prog << oracle

    for i in range(n):
        prog << H(qubits[i])

    counts = probRunDict(prog, qubits[:n - 1])
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
