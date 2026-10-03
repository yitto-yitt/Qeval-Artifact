# EVAL_META: task_id=112, framework=cirq, class=3
import numpy as np
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit(cirq.I(q) for q in qubits)

    pauli_gates = {
        "X": cirq.X,
        "Y": cirq.Y,
        "Z": cirq.Z,
    }

    for pauli_string, time in zip(pauli_strings, times):
        terms = []
        for i, char in enumerate(pauli_string):
            if char != "I":
                terms.append(pauli_gates[char](qubits[i]))

        if terms:
            pauli = cirq.PauliString(*terms)
            circuit.append(
                cirq.PauliStringPhasor(
                    pauli,
                    exponent_neg=time / np.pi,
                    exponent_pos=-time / np.pi,
                )
            )
        else:
            circuit.append(cirq.GlobalPhaseOperation(coefficient=np.exp(-1j * time)))

    return circuit
