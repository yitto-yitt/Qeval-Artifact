# EVAL_META: task_id=78, framework=qpanda, class=3
import numpy as np
from pyqpanda3 import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            qc.cr1(-np.pi / (2 ** (k - j)), k, j)
        qc.h(j)
    return qc
