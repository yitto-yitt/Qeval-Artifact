# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    pauli_map = {
        'I': cirq.I,
        'X': cirq.X,
        'Y': cirq.Y,
        'Z': cirq.Z,
    }

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli string is little-endian: rightmost char is qubit 0.
        # Map qubit index q to character at position len-1-q.
        ps = pauli_string
        L = len(ps)

        for _ in range(reps):
            # Effective evolution exp(-i * H * time / reps) for H = pauli
            t = time / reps

            # Build PauliString operator
            qubit_paulis = {}
            for q in range(L):
                ch = ps[L - 1 - q]
                if ch != 'I':
                    qubit_paulis[qubits[q]] = pauli_map[ch]

            if not qubit_paulis:
                # Identity term: global phase exp(-i * t)
                circuit.append(cirq.global_phase_operation(np.exp(-1j * t)))
                continue

            pauli_op = cirq.PauliString(qubit_paulis)
            # exp(-i * t * P) = PauliStringPhasor with exponent -t/pi * 2? 
            # cirq.PauliStringPhasor applies exp(i * pi * exponent_neg * P)
            # Use cirq's exponentiation: P**(exponent) gives exp(i*pi*exponent*(P-1)/...)
            # Safer: use PauliStringPhasor
            gate = cirq.PauliStringPhasor(
                pauli_op,
                exponent_neg=t / np.pi,
                exponent_pos=-t / np.pi,
            )
            circuit.append(gate)

    return circuit
