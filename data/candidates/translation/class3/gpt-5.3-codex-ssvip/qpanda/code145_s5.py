# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *

def qft_inverse(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    prog = QProg()
    for i in range(n // 2):
        prog << SWAP(q[i], q[n - i - 1])
    for j in range(n):
        for k in range(j):
            prog << CR(q[j], q[k], -3.141592653589793 / (2 ** (j - k)))
        prog << H(q[j])
    return prog
