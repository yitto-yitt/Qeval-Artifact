# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for pauli_str, time in zip(pauli_strings, times):
        reversed_str = pauli_str[::-1]
        pauli_dict = {}
        for i, char in enumerate(reversed_str):
            if char == 'X':
                pauli_dict[qubits[i]] = cirq.X
            elif char == 'Y':
                pauli_dict[qubits[i]] = cirq.Y
            elif char == 'Z':
                pauli_dict[qubits[i]] = cirq.Z
        if pauli_dict:
            ps = cirq.PauliString(pauli_dict)
            gate = cirq.PauliStringPhasor(ps, exponent=-time / np.pi)
            circuit.append(gate)
    return circuit
