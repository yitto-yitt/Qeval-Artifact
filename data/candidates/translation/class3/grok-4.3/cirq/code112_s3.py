# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    for pstr, t in zip(pauli_strings, times):
        pauli_map = {}
        for idx, char in enumerate(pstr):
            if char == 'X':
                pauli_map[qubits[idx]] = cirq.X
            elif char == 'Y':
                pauli_map[qubits[idx]] = cirq.Y
            elif char == 'Z':
                pauli_map[qubits[idx]] = cirq.Z
        if pauli_map:
            ps = cirq.PauliString(pauli_map)
            delta = t / reps if reps > 0 else t
            for _ in range(reps):
                circuit.append(ps ** (2 * delta / np.pi))
    return circuit
