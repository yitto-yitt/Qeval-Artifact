# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            qc.cp(-2 * np.pi / 2 ** (j - i), j, i)
        qc.h(i)
    return qc
