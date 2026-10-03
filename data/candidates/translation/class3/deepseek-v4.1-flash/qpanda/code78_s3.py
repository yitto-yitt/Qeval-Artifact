# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, qAlloc_many, H, CR

def qft_no_swaps(num_qubits):
    cir = QCircuit()
    qubits = qAlloc_many(num_qubits)
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -math.pi / (2 ** (k - j))
            cir << CR(qubits[k], qubits[j], angle)
        cir << H(qubits[j])
    return cir
