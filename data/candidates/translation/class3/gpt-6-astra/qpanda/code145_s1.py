# EVAL_META: task_id=145, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, SWAP, CNOT, U3

def qft_inverse(n):
    circuit = QCircuit()

    for j in range(n // 2):
        circuit << SWAP(j, n - j - 1)

    for j in range(n):
        for k in range(j):
            angle = -pi / (2 ** (j - k))
            circuit << U3(k, 0.0, 0.0, angle / 2)
            circuit << U3(j, 0.0, 0.0, angle / 2)
            circuit << CNOT(k, j)
            circuit << U3(j, 0.0, 0.0, -angle / 2)
            circuit << CNOT(k, j)
        circuit << H(j)

    return circuit
