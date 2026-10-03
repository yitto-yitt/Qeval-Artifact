# EVAL_META: task_id=116, framework=cirq, class=3
import cirq

def synthesize_evolution_gate(pauli_string, time):
    pauli_string = pauli_string.upper()
    qubits = cirq.LineQubit.range(len(pauli_string))
    circuit = cirq.Circuit()

    for q, char in zip(qubits, pauli_string):
        if char == 'X':
            circuit.append(cirq.H(q))
        elif char == 'Y':
            circuit.append(cirq.S(q) ** -1)
            circuit.append(cirq.H(q))

    non_id_qubits = [q for q, char in zip(qubits, pauli_string) if char != 'I']
    k = len(non_id_qubits)

    if k > 0:
        target = non_id_qubits[-1]
        for i in range(k - 1):
            circuit.append(cirq.CNOT(non_id_qubits[i], target))
        circuit.append(cirq.rz(2 * time)(target))
        for i in reversed(range(k - 1)):
            circuit.append(cirq.CNOT(non_id_qubits[i], target))

    for q, char in zip(qubits, pauli_string):
        if char == 'X':
            circuit.append(cirq.H(q))
        elif char == 'Y':
            circuit.append(cirq.H(q))
            circuit.append(cirq.S(q))

    return circuit
