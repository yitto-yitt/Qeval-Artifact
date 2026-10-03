# EVAL_META: task_id=112, framework=cirq, class=3
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    circuit.append([cirq.I(q) for q in qubits])

    for pauli_string, time in zip(pauli_strings, times):
        active = [q for q, p in zip(qubits, pauli_string) if p != 'I']

        # Basis change V^dagger
        for q, p in zip(qubits, pauli_string):
            if p == 'X':
                circuit.append(cirq.H(q))
            elif p == 'Y':
                circuit.append(cirq.S(q) ** -1)
                circuit.append(cirq.H(q))

        if active:
            target = active[0]
            for q in active[1:]:
                circuit.append(cirq.CNOT(q, target))
            circuit.append(cirq.rz(2 * time)(target))
            for q in active[1:]:
                circuit.append(cirq.CNOT(q, target))
        else:
            circuit.append(cirq.global_phase_operation(-time))

        # Basis change V
        for q, p in zip(qubits, pauli_string):
            if p == 'X':
                circuit.append(cirq.H(q))
            elif p == 'Y':
                circuit.append(cirq.H(q))
                circuit.append(cirq.S(q))

    return circuit
