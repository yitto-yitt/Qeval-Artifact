# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    pauli_map = {
        'I': cirq.I,
        'X': cirq.X,
        'Y': cirq.Y,
        'Z': cirq.Z,
    }

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli string is little-endian: rightmost char is qubit 0
        chars = pauli_string[::-1]
        qubit_ops = {}
        for i, ch in enumerate(chars):
            if ch != 'I':
                qubit_ops[qubits[i]] = pauli_map[ch]

        if not qubit_ops:
            continue

        ps = cirq.PauliString(qubit_ops)
        # PauliEvolutionGate with LieTrotter reps applies exp(-i * time * P)
        # split into reps steps of angle time/reps
        angle = time / reps
        for _ in range(reps):
            circuit.append(cirq.PauliStringPhasor(
                ps,
                exponent_neg=(angle / np.pi),
                exponent_pos=(-angle / np.pi),
            ))

    return circuit
