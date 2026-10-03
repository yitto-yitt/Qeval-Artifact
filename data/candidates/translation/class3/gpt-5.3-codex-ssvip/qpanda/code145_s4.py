# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, SWAP, CR


def qft_inverse(n):
    qc = QCircuit()
    for i in range(n // 2):
        qc.insert(SWAP(i, n - i - 1))
    for j in range(n):
        for k in range(j):
            qc.insert(CR(j, k, -3.141592653589793 / (2 ** (j - k))))
        qc.insert(H(j))
    return qc
