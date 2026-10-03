# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    qubits = cirq.LineQubit.range(len(pauli_string))
    pauli_map = {'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    
    pauli_ops = []
    for i, char in enumerate(pauli_string):
        if char in pauli_map:
            pauli_ops.append(pauli_map[char](qubits[i]))
            
    if not pauli_ops:
        return cirq.Circuit()
        
    pauli_string_obj = cirq.PauliString(pauli_ops)
    exponent = 2 * time / np.pi
    op = pauli_string_obj ** exponent
    
    try:
        circuit = cirq.Circuit(cirq.decompose(op))
    except TypeError:
        circuit = cirq.Circuit(op)
        
    return circuit
