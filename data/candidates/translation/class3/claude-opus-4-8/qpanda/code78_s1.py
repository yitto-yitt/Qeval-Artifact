# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, P

def qft_no_swaps(num_qubits):
    circ = QCircuit(num_qubits)
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -np.pi / (2 ** (k - j))
            circ << P(k, angle).control(j)
        circ << H(j)
    return circ
