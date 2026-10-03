# EVAL_META: task_id=112, framework=cirq, class=3
import math
import cmath
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0]) if pauli_strings else 0
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        step_time = time / reps
        
        pauli_dict = {}
        for idx, char in enumerate(pauli_string):
            if char == 'X':
                pauli_dict[qubits[num_qubits - 1 - idx]] = cirq.X
            elif char == 'Y':
                pauli_dict[qubits[num_qubits - 1 - idx]] = cirq.Y
            elif char == 'Z':
                pauli_dict[qubits[num_qubits - 1 - idx]] = cirq.Z
        
        for _ in range(reps):
            if pauli_dict:
                pauli_op = cirq.PauliString(pauli_dict)
                exponent = 2 * step_time / math.pi
                circuit.append(pauli_op ** exponent)
            else:
                circuit.append(cirq.global_phase_operation(cmath.exp(-1j * step_time)))
                
    return circuit
