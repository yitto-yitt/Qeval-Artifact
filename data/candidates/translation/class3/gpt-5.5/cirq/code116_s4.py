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
    if n == 0:
        return cirq.Circuit(cirq.global_phase_operation(np.exp(-1j * time)))

    pauli_op = np.array([[1]], dtype=complex)
    for char in pauli_string:
        pauli_op = np.kron(pauli_op, pauli_matrices[char])

    dim = 2 ** n
    unitary = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * pauli_op

    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(unitary)
    return cirq.Circuit(gate.on(*qubits))
