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

    label = pauli_string[::-1]
    n = len(label)

    mat = np.array([[1]], dtype=complex)
    for ch in label:
        mat = np.kron(paulis[ch], mat)

    unitary = expm(-1j * time * mat)

    qubits = [cirq.LineQubit(i) for i in range(n)]
    gate = cirq.MatrixGate(unitary, name='PauliEvolution')

    circuit = cirq.Circuit()
    circuit.append(gate.on(*qubits))
    return circuit
