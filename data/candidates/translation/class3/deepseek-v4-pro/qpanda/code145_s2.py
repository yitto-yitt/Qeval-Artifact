# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, CPUQVM, H, CP, SWAP

_QM = None

def qft_inverse(n):
    global _QM
    if _QM is None:
        _QM = CPUQVM()
        _QM.init_qvm()

    q = _QM.qAlloc_many(n)
    circ = QCircuit()

    for i in range(n // 2):
        circ << SWAP(q[i], q[n - 1 - i])

    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -2.0 * math.pi / (2 ** (k - j + 1))
            circ << CP(q[k], q[j], angle)
        circ << H(q[j])

    return circ
