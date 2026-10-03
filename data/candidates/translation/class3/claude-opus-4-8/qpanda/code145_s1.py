# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CR, SWAP
import numpy as np

def qft_inverse(n):
    circ = QCircuit(n)
    for i in range(n // 2):
        circ << SWAP(i, n - 1 - i)
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            circ << CR(k, j, angle)
        circ << H(j)
    return circ
