# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.I.on_each(*qubits))
    for pauli_str, time in zip(pauli_strings, times):
        pauli_map = {}
        for i, char in enumerate(pauli_str):
            if char == 'I':
                continue
            qubit = qubits[n - 1 - i]
            if char == 'X':
                pauli_map[qubit] = cirq.X
            elif char == 'Y':
                pauli_map[qubit] = cirq.Y
            elif char == 'Z':
                pauli_map[qubit] = cirq.Z
            else:
                raise ValueError(f"Unknown Pauli character: {char}")
        if not pauli_map:
            continue
        pauli_string_obj = cirq.PauliString(pauli_map)
        for _ in range(reps):
            t = time / reps
            gate = cirq.PauliStringPhasor(
                pauli_string_obj,
                exponent_neg=t / np.pi,
                exponent_pos=-t / np.pi
            )
            circuit.append(gate.on(*pauli_string_obj.qubits))
    return circuit
