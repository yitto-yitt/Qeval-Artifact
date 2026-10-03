# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    pauli_matrices = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }
    mat = np.array([[1.0 + 0j]])
    for p in pauli_string:
        mat = np.kron(mat, pauli_matrices[p])
    unitary = np.cos(time) * np.eye(2**n, dtype=complex) - 1j * np.sin(time) * mat
    gate = cirq.MatrixGate(unitary)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
