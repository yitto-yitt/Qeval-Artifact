# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }
    n = len(pauli_string)
    if n == 0:
        return cirq.Circuit()
    P = np.array([[1.0]], dtype=complex)
    for ch in pauli_string:
        P = np.kron(P, pauli_matrices[ch])
    dim = 2 ** n
    U = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * P
    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(U)
    return cirq.Circuit(gate.on(*qubits))
