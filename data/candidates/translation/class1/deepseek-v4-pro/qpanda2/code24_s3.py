# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    n = getattr(oracle, "num_qubits", None)
    if callable(n):
        try:
            n = n()
        except Exception:
            n = None
    if n is None:
        n = getattr(oracle, "n_qubits", None)
        if callable(n):
            try:
                n = n()
            except Exception:
                n = None
    if n is None:
        try:
            n = oracle.getQubitNum()
        except Exception:
            pass
    if n is None:
        try:
            used_qubits = oracle.get_used_qubits()
            if used_qubits and hasattr(used_qubits, "__len__"):
                n = len(used_qubits)
        except Exception:
            pass
    if n is None:
        raise ValueError("Cannot determine oracle qubit count")

    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n - 1)

    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])

    if callable(oracle):
        oracle(prog, qubits)
    else:
        prog << oracle

    for i in range(n):
        prog << H(qubits[i])

    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
