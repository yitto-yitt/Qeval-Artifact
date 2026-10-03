# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, controlled, RZ
import math

def qft_inverse(n):
    qc = QCircuit()
    q = [i for i in range(n)]
    for i in range(n // 2):
        qc << SWAP(q[i], q[n - i - 1])
    for j in range(n):
        for k in range(j):
            theta = -math.pi / (2 ** (j - k))
            qc << controlled(RZ(q[j], theta), [q[k]])
        qc << H(q[j])
    return qc
