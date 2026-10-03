# EVAL_META: task_id=145, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_allocated_qubits = []

def qft_inverse(n):
    if n <= 0:
        return QCircuit()
    q = machine.qAlloc_many(n)
    _allocated_qubits.append(q)
    cir = QCircuit()
    # Undo the final QFT swaps (swap is self-inverse)
    for i in range(n // 2):
        cir << SWAP(q[i], q[n - 1 - i])
    # Inverse QFT stages
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            cir << CP(q[j], q[i], -math.pi / (2 ** (j - i)))
        cir << H(q[i])
    return cir

machine.finalize()
