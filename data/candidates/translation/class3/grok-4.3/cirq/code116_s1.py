# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
from functools import reduce

def synthesize_evolution_gate(pauli_string, time):
    pauli_matrices = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    matrices = [pauli_matrices[p] for p in pauli_string]
    P = reduce(np.kron, matrices)
    c = np.cos(time)
    s = np.sin(time)
    U = c * np.eye(P.shape[0], dtype=complex) - 1j * s * P
    qubits = cirq.LineQubit.range(len(pauli_string))
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
