# EVAL_META: task_id=145, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit

def qft_inverse(n):
    qc = QuantumCircuit(n)
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    for j in range(n - 1, -1, -1):
        qc.h(j)
        for k in range(j - 1, -1, -1):
            qc.cp(j, k, math.pi / (2 ** (j - k)))
    return qc
