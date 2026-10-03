# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    pauli_map = {}
    for i, p in enumerate(pauli_string):
        if p == "X":
            pauli_map[qubits[i]] = cirq.X
        elif p == "Y":
            pauli_map[qubits[i]] = cirq.Y
        elif p == "Z":
            pauli_map[qubits[i]] = cirq.Z
    if not pauli_map:
        return cirq.Circuit()
    pauli = cirq.PauliString(pauli_map)
    pauli_mat = cirq.unitary(pauli)
    dim = 2 ** n
    identity = np.eye(dim)
    unitary = np.cos(time) * identity - 1j * np.sin(time) * pauli_mat
    gate = cirq.MatrixGate(unitary)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
