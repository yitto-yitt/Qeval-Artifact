# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def _pauli_from_char(ch, q):
        if ch == "I":
            return cirq.I(q)
        if ch == "X":
            return cirq.X(q)
        if ch == "Y":
            return cirq.Y(q)
        if ch == "Z":
            return cirq.Z(q)
        raise ValueError(f"Unsupported Pauli character: {ch}")

    for pauli_string, time in zip(pauli_strings, times):
        ps = cirq.PauliString(
            _pauli_from_char(ch, qubits[i]) for i, ch in enumerate(pauli_string)
        )
        if len(ps) == 0:
            continue
        for _ in range(reps):
            circuit.append(cirq.PauliStringPhasor(ps, exponent_neg=-time / np.pi, exponent_pos=time / np.pi))

    return circuit
