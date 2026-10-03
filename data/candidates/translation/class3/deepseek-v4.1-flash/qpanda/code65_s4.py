# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CR, SWAP
from math import pi

def QFT(n):
    circuit = QCircuit(n)
    for i in range(n - 1, -1, -1):
        circuit << H(i)
        for j in range(i):
            circuit << CR(j, i, pi / 2 ** (i - j))
    for i in range(n // 2):
        circuit << SWAP(i, n - i - 1)
    return circuit
