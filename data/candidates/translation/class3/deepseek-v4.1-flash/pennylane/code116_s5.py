# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    n = len(pauli_string)
    H = np.array([[1]], dtype=complex)
    for p in pauli_string:
        H = np.kron(H, pauli_matrices[p])
    U = expm(-1j * time * H)
    def circuit():
        qml.QubitUnitary(U, wires=range(n))
    return circuit
