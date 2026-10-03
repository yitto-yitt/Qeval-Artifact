# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, CR


def qft_inverse(n):
    circ = QCircuit()
    for i in range(n // 2):
        circ.insert(SWAP(i, n - i - 1))
    for j in range(n):
        for m in range(j):
            circ.insert(CR(j, m, -3.141592653589793 / (2 ** (j - m))))
        circ.insert(H(j))
    return circ
