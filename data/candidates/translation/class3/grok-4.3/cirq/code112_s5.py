# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for pauli_string, time in zip(pauli_strings, times):
        pauli_map = {}
        for idx, p in enumerate(pauli_string):
            if p == 'X':
                pauli_map[qubits[idx]] = cirq.X
            elif p == 'Y':
                pauli_map[qubits[idx]] = cirq.Y
            elif p == 'Z':
                pauli_map[qubits[idx]] = cirq.Z
        ps = cirq.PauliString(pauli_map)
        dt = time / reps if reps != 0 else time
        for _ in range(reps):
            exponent = 2 * dt / math.pi
            circuit.append(cirq.PauliStringPhasor(ps, exponent=exponent))
    return circuit
