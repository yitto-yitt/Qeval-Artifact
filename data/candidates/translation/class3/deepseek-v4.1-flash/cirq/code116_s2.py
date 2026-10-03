# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    pauli_matrices = {
        'I': np.eye(2),
        'X': np.array([[0, 1], [1, 0]]),
        'Y': np.array([[0, -1j], [1j, 0]]),
        'Z': np.array([[1, 0], [0, -1]])
    }
    P = np.eye(1)
    for char in pauli_string:
        P = np.kron(P, pauli_matrices[char])
    U = np.cos(time) * np.eye(2**n) - 1j * np.sin(time) * P
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
