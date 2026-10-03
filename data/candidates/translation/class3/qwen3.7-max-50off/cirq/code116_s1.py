# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = cirq.LineQubit.range(n)
    
    pauli_map = {}
    for i, p in enumerate(pauli_string):
        if p == 'X':
            pauli_map[qubits[i]] = cirq.X
        elif p == 'Y':
            pauli_map[qubits[i]] = cirq.Y
        elif p == 'Z':
            pauli_map[qubits[i]] = cirq.Z
            
    ps = cirq.PauliString(pauli_map)
    matrix = ps.matrix(qubits)
    
    dim = 2**n
    exp_matrix = np.cos(time) * np.eye(dim) - 1j * np.sin(time) * matrix
    
    gate = cirq.MatrixGate(exp_matrix)
    circuit = cirq.Circuit(gate.on(*qubits))
    
    return circuit
