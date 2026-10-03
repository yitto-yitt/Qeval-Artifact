# EVAL_META: task_id=145, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, CP, SWAP

def qft_inverse(n):
    circ = QCircuit()
    for i in range(n // 2):
        circ << SWAP(i, n - i - 1)
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            circ << CP(-np.pi / (2 ** (k - j)), j, k)
        circ << H(j)
    return circ
