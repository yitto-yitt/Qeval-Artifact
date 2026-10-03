# EVAL_META: task_id=116, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    num_qubits = len(pauli_string)
    pauli_matrix = np.array([[1]], dtype=complex)

    for char in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, pauli_matrices[char])

    unitary = (
        np.cos(time) * np.eye(2**num_qubits, dtype=complex)
        - 1j * np.sin(time) * pauli_matrix
    )

    return qml.tape.QuantumScript(
        [qml.QubitUnitary(unitary, wires=list(range(num_qubits)))],
        []
    )
