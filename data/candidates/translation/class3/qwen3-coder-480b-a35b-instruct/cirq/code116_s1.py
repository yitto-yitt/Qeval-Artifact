# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Map Pauli characters to Cirq gates
    pauli_map = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    
    # Create the Pauli string as a tensor product
    pauli_gates = [pauli_map[char] for char in pauli_string]
    
    # Create the Pauli string operation
    pauli_op = cirq.PauliString(dict(enumerate(pauli_gates)))
    
    # Create the evolution gate
    evolution_gate = cirq.PauliStringPhasor(pauli_op, exponent=-time/np.pi)
    
    # Create circuit and add the evolution gate
    qc = cirq.Circuit()
    qc.append(evolution_gate)
    
    return qc
