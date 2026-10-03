# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def pauli_string_evolution(pauli_str, time, qubits):
        n = len(qubits)
        sub_circuit = cirq.Circuit()
        involved = [(i, pauli_str[i]) for i in range(n) if pauli_str[i] != 'I']
        if not involved:
            return sub_circuit
        for i, p in involved:
            if p == 'X':
                sub_circuit.append(cirq.H(qubits[i]))
            elif p == 'Y':
                sub_circuit.append(cirq.rx(np.pi/2).on(qubits[i]))
        involved_qubits = [qubits[i] for i, _ in involved]
        for j in range(len(involved_qubits) - 1):
            sub_circuit.append(cirq.CNOT(involved_qubits[j], involved_qubits[j+1]))
        sub_circuit.append(cirq.rz(2 * time).on(involved_qubits[-1]))
        for j in reversed(range(len(involved_qubits) - 1)):
            sub_circuit.append(cirq.CNOT(involved_qubits[j], involved_qubits[j+1]))
        for i, p in involved:
            if p == 'X':
                sub_circuit.append(cirq.H(qubits[i]))
            elif p == 'Y':
                sub_circuit.append(cirq.rx(-np.pi/2).on(qubits[i]))
        return sub_circuit

    for pauli_str, time in zip(pauli_strings, times):
        reversed_pauli = pauli_str[::-1]
        for _ in range(reps):
            circuit += pauli_string_evolution(reversed_pauli, time / reps, qubits)
    return circuit
