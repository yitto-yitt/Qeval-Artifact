# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }
    matrices = [pauli_matrices[p] for p in pauli_string]
    pauli_matrix = matrices[0]
    for m in matrices[1:]:
        pauli_matrix = np.kron(pauli_matrix, m)
    n = len(pauli_string)
    identity = np.eye(2 ** n, dtype=complex)
    evolution_matrix = np.cos(time) * identity - 1j * np.sin(time) * pauli_matrix
    gate = cirq.MatrixGate(evolution_matrix)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
