# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    n = len(pauli_string)
    pauli_matrix = np.array([[1]], dtype=complex)
    for p in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, pauli_matrices[p])

    unitary = np.cos(time) * np.eye(2**n, dtype=complex) - 1j * np.sin(time) * pauli_matrix

    qubits = cirq.LineQubit.range(n)
    return cirq.Circuit(cirq.MatrixGate(unitary).on(*qubits))
