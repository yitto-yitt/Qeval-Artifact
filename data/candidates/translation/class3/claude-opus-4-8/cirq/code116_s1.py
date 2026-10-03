# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
    }

    n = len(pauli_string)
    # Qiskit Pauli string is little-endian: rightmost char is qubit 0
    mat = np.array([[1]], dtype=complex)
    for ch in pauli_string:
        mat = np.kron(mat, paulis[ch])

    U = expm(-1j * time * mat)

    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(U, name='exp')
    circuit = cirq.Circuit()
    circuit.append(gate.on(*qubits))
    return circuit
