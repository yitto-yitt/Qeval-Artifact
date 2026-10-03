# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for pstr, t in zip(pauli_strings, times):
        pauli_dict = {}
        for idx, char in enumerate(pstr):
            if char == 'X':
                pauli_dict[qubits[idx]] = cirq.X
            elif char == 'Y':
                pauli_dict[qubits[idx]] = cirq.Y
            elif char == 'Z':
                pauli_dict[qubits[idx]] = cirq.Z
        pauli_string = cirq.PauliString(pauli_dict)
        exponent = 2 * t / math.pi
        phasor = cirq.PauliStringPhasor(pauli_string, exponent=exponent)
        circuit.append(phasor)
    return circuit
