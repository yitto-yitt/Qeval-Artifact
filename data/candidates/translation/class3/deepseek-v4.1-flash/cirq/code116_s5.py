# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
import scipy.linalg

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    pauli_matrices = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    # Build Pauli operator matrix using Qiskit's little-endian convention:
    # rightmost character corresponds to qubit 0.
    P = np.array([[1]], dtype=complex)
    for char in reversed(pauli_string):
        if char not in pauli_matrices:
            raise ValueError(f"Invalid Pauli character: {char}")
        P = np.kron(P, pauli_matrices[char])
    # Compute exp(-i * time * P)
    U = scipy.linalg.expm(-1j * time * P)
    # Create MatrixGate and circuit
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
