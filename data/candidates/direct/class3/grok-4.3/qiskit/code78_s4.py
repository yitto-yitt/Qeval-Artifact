# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def qft_no_swaps(num_qubits):
    qc = QuantumCircuit(num_qubits)
    for qubit in range(num_qubits - 1, -1, -1):
        for next_qubit in range(num_qubits - 1, qubit, -1):
            qc.cp(-np.pi / 2**(next_qubit - qubit), next_qubit, qubit)
        qc.h(qubit)
    return qc
