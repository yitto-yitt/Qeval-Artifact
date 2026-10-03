# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins
def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    c = qvm.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])
    for i in range(n - 1):
        prog << Measure(q[i], c[i])
    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
