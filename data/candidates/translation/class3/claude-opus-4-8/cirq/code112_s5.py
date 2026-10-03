# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)

    pauli_map = {
        'I': cirq.I,
        'X': cirq.X,
        'Y': cirq.Y,
        'Z': cirq.Z,
    }

    circuit = cirq.Circuit()

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli strings are little-endian: rightmost char is qubit 0.
        chars = pauli_string[::-1]

        for _ in range(reps):
            # Build the PauliString term (identity components dropped).
            terms = {}
            for i, ch in enumerate(chars):
                if ch != 'I':
                    terms[qubits[i]] = pauli_map[ch]

            if not terms:
                continue

            pauli_str = cirq.PauliString(terms)
            # exp(-i * time * P), split into reps steps.
            exponent = -2.0 * time / reps / np.pi
            circuit += cirq.PauliStringPhasor(pauli_str, exponent_neg=exponent)

    return circuit
