# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QProg, Hadamard, SWAP, CPhase, CPUQVM

def qft_inverse(n):
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(n)
    prog = QProg()
    # Swaps first (inverse of the final swaps in QFT)
    for i in range(n // 2):
        prog << SWAP(q[i], q[n - 1 - i])
    # Inverse of the core QFT (with negative angles, reversed loop order)
    for i in range(n - 1, -1, -1):
        prog << Hadamard(q[i])
        for j in range(n - 1, i, -1):
            angle = -2.0 * math.pi / (2 ** (j - i + 1))
            prog << CPhase(q[j], q[i], angle)
    return prog
