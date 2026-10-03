# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for pauli_str, t in zip(pauli_strings, times):
        rev = pauli_str[::-1]
        pauli_dict = {}
        for i, char in enumerate(rev):
            if char == 'I':
                continue
            elif char == 'X':
                pauli_dict[qubits[i]] = cirq.X
            elif char == 'Y':
                pauli_dict[qubits[i]] = cirq.Y
            elif char == 'Z':
                pauli_dict[qubits[i]] = cirq.Z
            else:
                raise ValueError(f"Unknown Pauli character {char}")
        pauli_string = cirq.PauliString(pauli_dict)
        circuit.append(cirq.PauliStringPhasor(pauli_string, exponent=-t / np.pi))
    return circuit
