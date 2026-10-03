# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    for pauli_str, t in zip(pauli_strings, times):
        pauli_dict = {q: p for q, p in zip(qubits, pauli_str) if p != 'I'}
        pauli_string = cirq.PauliString(pauli_dict)
        pauli_sum = cirq.PauliSum.from_pauli_strings([pauli_string])
        circuit.append(
            cirq.PauliSumExponential(pauli_sum, exponent=-t / np.pi)
        )

    return circuit
