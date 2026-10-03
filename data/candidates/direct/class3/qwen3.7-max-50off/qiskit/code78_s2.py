# EVAL_META: task_id=78, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            qc.cp(-np.pi / (2 ** (k - j)), j, k)
        qc.h(j)
    return qc
