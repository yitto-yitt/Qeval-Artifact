# EVAL_META: task_id=145, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QCircuit, H, U1, CNOT, SWAP


def qft_inverse(n):
    circuit = QCircuit()

    for i in range(n // 2):
        circuit << SWAP(i, n - 1 - i)

    for j in range(n):
        for k in range(j):
            angle = -pi / (2 ** (j - k))
            circuit << U1(j, angle / 2)
            circuit << U1(k, angle / 2)
            circuit << CNOT(j, k)
            circuit << U1(k, -angle / 2)
            circuit << CNOT(j, k)
        circuit << H(j)

    return circuit
