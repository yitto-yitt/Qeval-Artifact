# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP
from pyqpanda3.core import RZ
import numpy as np


def _cp(control, target, theta):
    circ = QCircuit()
    circ << RZ(target, theta / 2)
    from pyqpanda3.core import CNOT
    circ << CNOT(control, target)
    circ << RZ(target, -theta / 2)
    circ << CNOT(control, target)
    circ << RZ(control, theta / 2)
    return circ


def qft_inverse(n):
    circ = QCircuit()
    for i in range(n // 2):
        circ << SWAP(i, n - 1 - i)
    for j in range(n):
        for m in range(j):
            circ << _cp(m, j, -np.pi / float(2 ** (j - m)))
        circ << H(j)
    return circ
