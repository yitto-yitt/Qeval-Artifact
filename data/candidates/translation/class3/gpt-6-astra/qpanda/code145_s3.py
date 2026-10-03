# EVAL_META: task_id=145, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, CR, SWAP

def qft_inverse(n):
    circuit = QCircuit()
    for i in range(n // 2):
        circuit << SWAP(i, n - i - 1)
    for j in range(n):
        for k in range(j):
            circuit << CR(j, k, -pi / (2 ** (j - k)))
        circuit << H(j)
    return circuit
