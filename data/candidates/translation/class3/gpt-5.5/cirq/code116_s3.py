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
    qubits = cirq.LineQubit.range(n)

    pauli_matrix = np.array([[1]], dtype=complex)
    for p in pauli_string:
        pauli_matrix = np.kron(pauli_matrix, pauli_matrices[p])

    dim = 2 ** n
    unitary = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * pauli_matrix

    circuit = cirq.Circuit()
    if n > 0:
        circuit.append(cirq.MatrixGate(unitary).on(*qubits))
    return circuit
