# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    qubits = cirq.LineQubit.range(len(pauli_strings[0]))
    circuit = cirq.Circuit(cirq.I.on_each(*qubits))
    pauli_gates = {"X": cirq.X, "Y": cirq.Y, "Z": cirq.Z}

    for label, time in zip(pauli_strings, times):
        if len(label) > len(qubits):
            raise ValueError("Pauli string exceeds the circuit width.")
        if any(char not in "IXYZ" for char in label):
            raise ValueError("Expected a Pauli string containing only I, X, Y, Z.")

        pauli = cirq.PauliString({
            qubits[index]: pauli_gates[char]
            for index, char in enumerate(reversed(label))
            if char != "I"
        })
        step_time = time / reps

        for _ in range(reps):
            if len(pauli) == 0:
                circuit.append(
                    cirq.global_phase_operation(np.exp(-1j * step_time))
                )
            else:
                circuit.append(
                    cirq.PauliStringPhasor(
                        pauli,
                        exponent_neg=step_time / np.pi,
                        exponent_pos=-step_time / np.pi,
                    )
                )

    return circuit
