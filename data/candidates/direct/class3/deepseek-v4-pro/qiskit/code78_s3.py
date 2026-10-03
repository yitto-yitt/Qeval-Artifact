# EVAL_META: task_id=78, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for j in range(num_qubits):
        qc.h(j)
        for k in range(j + 1, num_qubits):
            qc.cp(-np.pi / (2 ** (k - j)), k, j)
    return qc
