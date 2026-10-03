# EVAL_META: task_id=145, framework=qpanda2, class=3
from pyqpanda import *
import math
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_inverse(n):
    prog = create_empty_qprog()
    q = qubits[:n]
    for i in range(n//2):
        prog << SWAP(q[i], q[n-1-i])
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            lam = -math.pi / (2 ** (j - i))
            prog << CR(q[j], q[i], lam)
        prog << H(q[i])
    return prog
machine.finalize()
