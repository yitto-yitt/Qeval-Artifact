# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    pauli_map = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli strings are little-endian: rightmost char is qubit 0
        chars = pauli_string[::-1]
        angle_per_rep = (2.0 * time) / reps

        for _ in range(reps):
            terms = {}
            for i, ch in enumerate(chars):
                if ch != 'I':
                    terms[qubits[i]] = pauli_map[ch]
            if not terms:
                continue
            ps = cirq.PauliString(terms)
            # exp(-i * time * P) => PauliStringPhasor with exponent = 2*time/pi
            gate = cirq.PauliStringPhasor(
                ps, exponent_neg=angle_per_rep / np.pi
            )
            circuit.append(gate)

    return circuit
