# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, CR


def qft_inverse(n):
    circuit = QCircuit()
    for i in range(n // 2):
        circuit.insert(SWAP(i, n - i - 1))
    for j in reversed(range(n)):
        circuit.insert(H(j))
        for m in reversed(range(j)):
            circuit.insert(CR(j, m, -3.141592653589793 / (2 ** (j - m))))
    return circuit
