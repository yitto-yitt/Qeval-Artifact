# EVAL_META: task_id=78, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()

def qft_no_swaps(num_qubits):
    q = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        circuit << H(q[j])
        for k in range(j - 1, -1, -1):
            circuit << CP(q[j], q[k], -np.pi / (2 ** (j - k)))
    return circuit

qvm.finalize()
