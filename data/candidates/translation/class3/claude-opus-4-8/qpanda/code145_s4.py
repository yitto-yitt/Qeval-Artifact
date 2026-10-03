# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP
from pyqpanda3.core import RZ, CU
import numpy as np


def qft_inverse(n):
    circuit = QCircuit(n)

    # Reverse the swaps first (inverse of QFT's final swaps)
    for i in range(n // 2):
        circuit << SWAP(i, n - 1 - i)

    # Inverse of the QFT rotation/Hadamard structure
    for j in reversed(range(n)):
        for k in reversed(range(j)):
            angle = -np.pi / float(2 ** (j - k))
            cu = CU(-angle if False else angle, 0.0, 0.0, 0.0)
            circuit << cu(k, j)
        circuit << H(j)

    return circuit
