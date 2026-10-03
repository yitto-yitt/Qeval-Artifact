# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QMachine, H, CR

def qft_no_swaps(num_qubits):
    qm = QMachine(num_qubits)
    q = qm.qAlloc_many(num_qubits)
    circ = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            circ << CR(angle, q[k], q[j])
        circ << H(q[j])
    return circ
