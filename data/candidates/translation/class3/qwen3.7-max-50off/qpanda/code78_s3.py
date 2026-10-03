# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QVec, H, CR

def qft_no_swaps(num_qubits):
    q = QVec(num_qubits)
    circ = QCircuit()
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            circ << CR(-np.pi / (2 ** (k - j)), q[k], q[j])
        circ << H(q[j])
    return circ
