# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit
import numpy as np

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for i in reversed(range(n)):
        for j in reversed(range(i + 1, n)):
            qc.cp(-np.pi / 2 ** (j - i), i, j)
        qc.h(i)
    return qc
