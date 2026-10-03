# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    pauli_map = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    n = len(pauli_string)
    if n == 0:
        return cirq.Circuit()
        
    mat = pauli_map[pauli_string[0]]
    for c in pauli_string[1:]:
        mat = np.kron(mat, pauli_map[c])
        
    U = expm(-1j * time * mat)
    
    qubits = cirq.LineQubit.range(n)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits))
    
    return circuit
