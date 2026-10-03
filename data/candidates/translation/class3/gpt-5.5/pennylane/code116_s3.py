# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    num_wires = len(pauli_string)
    pauli_matrix = np.array([[1]], dtype=complex)

    for char in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, pauli_matrices[char])

    dim = 2 ** num_wires
    unitary = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * pauli_matrix

    op = qml.QubitUnitary(unitary, wires=list(range(num_wires)))
    return qml.tape.QuantumScript([op])
