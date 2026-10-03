# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    matrices = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    pauli_matrix = np.array([[1]], dtype=complex)
    for char in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, matrices[char])

    dim = pauli_matrix.shape[0]
    unitary = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * pauli_matrix

    op = qml.QubitUnitary(unitary, wires=range(len(pauli_string)))
    return qml.tape.QuantumScript(ops=[op], measurements=[])
