# EVAL_META: task_id=78, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit


def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            qc.cp(-np.pi / (2 ** (j - i)), j, i)
        qc.h(i)
    return qc
