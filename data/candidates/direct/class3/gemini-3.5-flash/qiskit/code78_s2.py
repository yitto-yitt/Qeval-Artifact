# EVAL_META: task_id=78, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        for j in range(i):
            qc.cp(-np.pi / (2 ** (i - j)), j, i)
        qc.h(i)
    return qc
