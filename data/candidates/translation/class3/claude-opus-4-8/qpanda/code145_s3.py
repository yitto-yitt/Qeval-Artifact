# EVAL_META: task_id=145, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, CR, SWAP

def qft_inverse(n):
    circuit = QCircuit()
    # Build forward QFT then invert (dagger)
    forward = QCircuit()
    for j in range(n):
        forward << H(j)
        for k in range(j + 1, n):
            forward << CR(k, j, np.pi / (2 ** (k - j)))
    for i in range(n // 2):
        forward << SWAP(i, n - 1 - i)
    circuit << forward.dagger()
    return circuit
