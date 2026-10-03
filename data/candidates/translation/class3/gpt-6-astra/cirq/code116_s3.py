# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    operator = np.ones((1, 1), dtype=complex)
    for label in pauli_string:
        if label not in paulis:
            raise ValueError("Pauli string must contain only I, X, Y, and Z.")
        operator = np.kron(operator, paulis[label])

    unitary = expm(-1j * float(time) * operator)
    qubits = cirq.LineQubit.range(len(pauli_string))
    if not qubits:
        return cirq.Circuit(cirq.global_phase_operation(unitary[0, 0]))
    return cirq.Circuit(cirq.MatrixGate(unitary).on(*qubits))
