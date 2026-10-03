# EVAL_META: task_id=78, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, H, CR

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def qft_no_swaps(num_qubits):
    circ = QCircuit()
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -np.pi / (2 ** (k - j))
            circ << CR(qubits[k], qubits[j], angle)
        circ << H(qubits[j])
    return circ


machine.finalize()
