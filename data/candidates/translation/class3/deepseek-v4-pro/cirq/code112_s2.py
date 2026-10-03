# EVAL_META: task_id=112, framework=cirq, class=3
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    for pauli_string, time in zip(pauli_strings, times):
        pauli_string = pauli_string.upper()
        active_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
        if not active_indices:
            continue

        active_qubits = [qubits[i] for i in active_indices]
        active_paulis = [pauli_string[i] for i in active_indices]
        time_per_rep = time / reps

        for _ in range(reps):
            # Change basis so each non-identity Pauli acts as Z
            for q, p in zip(active_qubits, active_paulis):
                if p == 'X':
                    circuit.append(cirq.H(q))
                elif p == 'Y':
                    circuit.append(cirq.S(q) ** -1)
                    circuit.append(cirq.H(q))

            # Parity CNOT cascade
            for control, target in zip(active_qubits, active_qubits[1:]):
                circuit.append(cirq.CNOT(control, target))

            # Rotate on the last active qubit
            circuit.append(cirq.rz(2 * time_per_rep)(active_qubits[-1]))

            # Uncompute CNOT cascade
            for control, target in reversed(list(zip(active_qubits, active_qubits[1:]))):
                circuit.append(cirq.CNOT(control, target))

            # Uncompute basis changes
            for q, p in reversed(list(zip(active_qubits, active_paulis))):
                if p == 'X':
                    circuit.append(cirq.H(q))
                elif p == 'Y':
                    circuit.append(cirq.H(q))
                    circuit.append(cirq.S(q))

    return circuit
