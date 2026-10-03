# EVAL_META: task_id=116, framework=cirq, class=3

import numpy as np
import cirq
from scipy.linalg import expm


_PAULI_MATRICES = {
    'I': np.array([[1, 0], [0, 1]], dtype=complex),
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, -1]], dtype=complex),
}


def synthesize_evolution_gate(pauli_string, time):
    """Synthesize exp(-i * time * Pauli(pauli_string)) as a Cirq circuit."""
    pauli_matrix = np.array([[1]], dtype=complex)
    for char in pauli_string:
        if char not in _PAULI_MATRICES:
            raise ValueError(f"Invalid Pauli character: {char}")
        pauli_matrix = np.kron(pauli_matrix, _PAULI_MATRICES[char])

    evolution_matrix = expm(-1j * time * pauli_matrix)

    qubits = cirq.LineQubit.range(len(pauli_string))
    gate = cirq.MatrixGate(evolution_matrix)
    return cirq.Circuit(gate.on(*qubits))
