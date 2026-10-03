# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, RZ, X

def qft_no_swaps(num_qubits):
    qc = QCircuit(num_qubits)
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            angle = -np.pi / (2 ** (k - j))
            controlled_rz = RZ(j, angle).control([k])
            qc << controlled_rz
        qc << H(j)
    return qc
