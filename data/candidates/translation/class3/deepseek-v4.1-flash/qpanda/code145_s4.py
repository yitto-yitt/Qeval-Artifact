# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, Qubit, H, SWAP, CR

def qft_inverse(n):
    q = [Qubit(i) for i in range(n)]
    circ = QCircuit()
    for i in range(n // 2):
        circ << SWAP(q[i], q[n - 1 - i])
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            circ << CR(q[j], q[i], -math.pi / (2 ** (j - i)))
        circ << H(q[i])
    return circ
