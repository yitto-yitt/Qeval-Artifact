# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    pauli_map = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}

    for pauli_string, time in zip(pauli_strings, times):
        ops = []
        for i, p in enumerate(pauli_string):
            if p != 'I':
                ops.append(pauli_map[p](qubits[i]))
        if not ops:
            continue
        pauli_product = ops[0]
        for op in ops[1:]:
            pauli_product *= op
        for _ in range(reps):
            circuit.append(cirq.PauliStringPhasor(pauli_product, exponent_neg=-time / np.pi, exponent_pos=time / np.pi))

    return circuit
