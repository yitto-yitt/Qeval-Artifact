# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    pauli_map = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    
    for pstr, time in zip(pauli_strings, times):
        ops = []
        for i, char in enumerate(reversed(pstr)):
            if char != 'I':
                ops.append(pauli_map[char](qubits[i]))
        
        if not ops:
            continue
            
        pauli_string = cirq.PauliString(ops)
        
        for _ in range(reps):
            t_step = time / reps
            gate = cirq.PauliStringPhasor(pauli_string, exponent_neg=2 * t_step / math.pi)
            circuit.append(gate)
            
    return circuit
