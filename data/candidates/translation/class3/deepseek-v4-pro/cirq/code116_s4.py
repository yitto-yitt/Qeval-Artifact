# EVAL_META: task_id=116, framework=cirq, class=3
import numpy as np
import cirq

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    non_i_indices = [i for i, p in enumerate(pauli_string) if p != 'I']

    for i, p in enumerate(pauli_string):
        if p == 'I':
            circuit.append(cirq.I(qubits[i]))

    if not non_i_indices:
        circuit.append(cirq.GlobalPhaseOperation(np.exp(-1j * time)))
        return circuit

    target_idx = non_i_indices[0]
    target = qubits[target_idx]

    for i in non_i_indices:
        q = qubits[i]
        p = pauli_string[i]
        if p == 'Y':
            circuit.append(cirq.S(q) ** -1)
        elif p == 'Z':
            circuit.append(cirq.H(q))

    for i in non_i_indices:
        if i == target_idx:
            continue
        circuit.append(cirq.CNOT(qubits[i], target))

    circuit.append(cirq.rx(2 * time).on(target))

    for i in reversed(non_i_indices):
        if i == target_idx:
            continue
        circuit.append(cirq.CNOT(qubits[i], target))

    for i in reversed(non_i_indices):
        q = qubits[i]
        p = pauli_string[i]
        if p == 'Y':
            circuit.append(cirq.S(q))
        elif p == 'Z':
            circuit.append(cirq.H(q))

    return circuit
