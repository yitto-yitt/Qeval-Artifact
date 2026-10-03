# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)

    pauli_map = {
        "I": np.array([[1, 0], [0, 1]], dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    hamiltonian = np.array([[1]], dtype=complex)
    for p in pauli_string:
        hamiltonian = np.kron(hamiltonian, pauli_map[p])

    eigvals, eigvecs = np.linalg.eigh(hamiltonian)
    unitary = eigvecs @ np.diag(np.exp(-1j * time * eigvals)) @ eigvecs.conj().T

    circuit = cirq.Circuit(cirq.MatrixGate(unitary).on(*qubits))
    return circuit
