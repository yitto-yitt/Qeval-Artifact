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
        # Qiskit Pauli string is little-endian: rightmost char -> qubit 0
        chars = pauli_string[::-1]

        exponent_scale = (2.0 * time) / (np.pi * reps)

        for _ in range(reps):
            for idx, ch in enumerate(chars):
                gate = pauli_map[ch]
                if gate is cirq.I:
                    continue
                circuit.append(
                    (gate ** exponent_scale).on(qubits[idx])
                    if False else None
                )
            # Build the PauliString-based exponential for correctness
            ps_terms = {}
            for idx, ch in enumerate(chars):
                if ch == 'I':
                    continue
                ps_terms[qubits[idx]] = pauli_map[ch]
            if not ps_terms:
                continue
            pauli_str = cirq.PauliString(ps_terms)
            circuit.append(
                cirq.PauliStringPhasor(
                    pauli_str,
                    exponent_neg=(2.0 * time) / (np.pi * reps),
                )
            )

    return circuit
