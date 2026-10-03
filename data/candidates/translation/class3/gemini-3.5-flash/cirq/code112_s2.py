# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        return cirq.Circuit()
    
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        pauli_string_obj = cirq.PauliString()
        for i, char in enumerate(pauli_string):
            if char == 'X':
                pauli_string_obj *= cirq.X(qubits[i])
            elif char == 'Y':
                pauli_string_obj *= cirq.Y(qubits[i])
            elif char == 'Z':
                pauli_string_obj *= cirq.Z(qubits[i])
        
        if not pauli_string_obj.qubits:
            continue
            
        exponent = 2 * (time / reps) / math.pi
        for _ in range(reps):
            circuit.append(pauli_string_obj ** exponent)
            
    return circuit
