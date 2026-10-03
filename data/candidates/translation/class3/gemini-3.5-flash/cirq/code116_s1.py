# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    qubits = cirq.LineQubit.range(len(pauli_string))
    pauli_map = {'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    
    ops = []
    for i, char in enumerate(reversed(pauli_string)):
        if char in pauli_map:
            ops.append(pauli_map[char](qubits[i]))
            
    circuit = cirq.Circuit()
    if ops:
        pauli_str = cirq.PauliString(ops)
        exponent = 2 * time / np.pi
        circuit.append(pauli_str ** exponent)
    else:
        circuit.append(cirq.global_phase_operation(np.exp(-1j * time)))
    return circuit
