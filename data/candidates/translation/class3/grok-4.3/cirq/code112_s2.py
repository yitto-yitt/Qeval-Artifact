# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    for pauli_str, t in zip(pauli_strings, times):
        dt = t / reps if reps > 0 else t
        for _ in range(reps):
            pauli_dict = {}
            for i, char in enumerate(pauli_str):
                if char == 'X':
                    pauli_dict[qubits[i]] = cirq.X
                elif char == 'Y':
                    pauli_dict[qubits[i]] = cirq.Y
                elif char == 'Z':
                    pauli_dict[qubits[i]] = cirq.Z
            pauli = cirq.PauliString(pauli_dict)
            if pauli:
                circuit.append(pauli ** (dt / np.pi))
    return circuit
