# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        pauli_dict = {}
        for i in range(num_qubits):
            char = pauli_string[num_qubits - 1 - i]
            q = qubits[i]
            if char == 'X':
                pauli_dict[q] = cirq.X
            elif char == 'Y':
                pauli_dict[q] = cirq.Y
            elif char == 'Z':
                pauli_dict[q] = cirq.Z
        
        if not pauli_dict:
            continue
            
        pauli_string_obj = cirq.PauliString(pauli_dict)
        exponent = 2.0 * (time / reps) / np.pi
        op = pauli_string_obj ** exponent
        for _ in range(reps):
            circuit.append(op)
            
    return circuit
