# EVAL_META: task_id=116, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    matrices = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    pauli_matrix = np.ones((1, 1), dtype=complex)
    for label in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, matrices[label])

    unitary = expm(-1j * time * pauli_matrix)
    return qml.tape.QuantumScript(
        [qml.QubitUnitary(unitary, wires=range(len(pauli_string)))]
    )
