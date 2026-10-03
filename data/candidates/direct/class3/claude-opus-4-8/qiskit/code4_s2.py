# EVAL_META: task_id=4, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]], dtype=complex)
    gate = Operator(matrix).to_instruction()
    qc = QuantumCircuit(2)
    qc.append(gate, [0, 1])
    return qc
