# EVAL_META: task_id=116, framework=cirq, class=3
import numpy as np
import cirq

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    # Global phase for all-identity string is irrelevant
    if all(c == 'I' for c in pauli_string):
        return circuit

    non_id = [i for i, c in enumerate(pauli_string) if c != 'I']
    first = qubits[non_id[0]]

    # Map each non-identity Pauli to Z
    for i in non_id:
        c = pauli_string[i]
        q = qubits[i]
        if c == 'X':
            circuit.append(cirq.H(q))
        elif c == 'Y':
            circuit.append(cirq.rx(np.pi / 2).on(q))
        # 'Z' needs no basis change

    # CNOT ladder to collect Z factors onto the first qubit
    for i in non_id[1:]:
        circuit.append(cirq.CNOT(qubits[i], first))

    # Rotation by 2 * time on the accumulated Z
    circuit.append(cirq.rz(2 * time).on(first))

    # Uncompute CNOTs
    for i in reversed(non_id[1:]):
        circuit.append(cirq.CNOT(qubits[i], first))

    # Restore original Pauli basis
    for i in non_id:
        c = pauli_string[i]
        q = qubits[i]
        if c == 'X':
            circuit.append(cirq.H(q))
        elif c == 'Y':
            circuit.append(cirq.rx(-np.pi / 2).on(q))
        # 'Z' already unchanged

    return circuit
