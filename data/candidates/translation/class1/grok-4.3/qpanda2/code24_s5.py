# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    qubits = oracle.get_qubits()
    n = len(qubits)
    qvm = CPUQVM()
    qvm.init_qvm()
    cbits = qvm.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(qubits[n - 1])
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
