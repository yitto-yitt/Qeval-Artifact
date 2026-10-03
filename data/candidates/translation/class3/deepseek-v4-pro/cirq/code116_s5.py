# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np


def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    non_i = [i for i, p in enumerate(pauli_string) if p != 'I']

    # Identity Pauli string: exp(-i*time*I) is a global phase.
    if not non_i:
        if n > 0:
            circuit.append(cirq.MatrixGate(np.exp(-1j * time) * np.eye(2)).on(qubits[0]))
            for q in qubits[1:]:
                circuit.append(cirq.I(q))
        return circuit

    # Basis transformations: map X/Y Paulis to Z.
    for i in non_i:
        p = pauli_string[i]
        if p == 'X':
            circuit.append(cirq.H(qubits[i]))
        elif p == 'Y':
            circuit.append(cirq.rx(np.pi / 2).on(qubits[i]))

    target = qubits[non_i[-1]]

    # Compute parity into target qubit.
    if len(non_i) > 1:
        for i in non_i[:-1]:
            circuit.append(cirq.CNOT(qubits[i], target))

    # Evolve the diagonal Z-only Pauli string.
    circuit.append(cirq.rz(2 * time).on(target))

    # Uncompute parity.
    if len(non_i) > 1:
        for i in reversed(non_i[:-1]):
            circuit.append(cirq.CNOT(qubits[i], target))

    # Undo basis transformations.
    for i in reversed(non_i):
        p = pauli_string[i]
        if p == 'X':
            circuit.append(cirq.H(qubits[i]))
        elif p == 'Y':
            circuit.append(cirq.rx(-np.pi / 2).on(qubits[i]))

    # Ensure identity qubits are present in the circuit.
    for i, p in enumerate(pauli_string):
        if p == 'I':
            circuit.append(cirq.I(qubits[i]))

    return circuit
