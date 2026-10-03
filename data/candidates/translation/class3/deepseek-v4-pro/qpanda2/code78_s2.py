# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

qvm = CPUQVM()
qvm.init_qvm()

def qft_no_swaps(num_qubits):
    q = qvm.qAlloc_many(num_qubits)
    circ = QCircuit()

    for j in range(num_qubits):
        ctrl = q[num_qubits - 1 - j]
        circ << H(ctrl)
        for k in range(j + 1, num_qubits):
            target = q[num_qubits - 1 - k]
            angle = -np.pi / (2 ** (k - j))
            circ << CP(ctrl, target, angle)

    return circ

qvm.finalize()
