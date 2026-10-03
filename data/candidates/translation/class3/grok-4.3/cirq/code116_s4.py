# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = cirq.LineQubit.range(n_qubits)
    pauli_map = {}
    for idx, char in enumerate(pauli_string):
        if char == 'X':
            pauli_map[qubits[idx]] = cirq.X
        elif char == 'Y':
            pauli_map[qubits[idx]] = cirq.Y
        elif char == 'Z':
            pauli_map[qubits[idx]] = cirq.Z
    if not pauli_map:
        pauli_matrix = np.eye(2 ** n_qubits, dtype=complex)
    else:
        pauli = cirq.PauliString(pauli_map)
        pauli_matrix = pauli.matrix(qubit_order=qubits)
    theta = time
    identity = np.eye(2 ** n_qubits, dtype=complex)
    unitary = np.cos(theta) * identity - 1j * np.sin(theta) * pauli_matrix
    gate = cirq.MatrixGate(unitary)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
