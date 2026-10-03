# EVAL_META: task_id=145, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, SWAP, CR

def qft_inverse(n):
    qc = QCircuit(n)
    for i in range(n // 2):
        qc << SWAP(i, n - 1 - i)
    for j in range(n - 1, -1, -1):
        for k in range(n - 1, j, -1):
            qc << CR(k, j, -np.pi / (2 ** (k - j))).dagger()
        qc << H(j)
    return qc
