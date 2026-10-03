# EVAL_META: task_id=116, framework=cirq, class=3
import numpy as np
import cirq

def synthesize_evolution_gate(pauli_string, time):
    pauli_map = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    num_qubits = len(pauli_string)
    if num_qubits == 0:
        return cirq.Circuit()
        
    mat_P = np.array([[1]], dtype=complex)
    for char in pauli_string:
        mat_P = np.kron(mat_P, pauli_map[char])
        
    dim = 2 ** num_qubits
    U = np.cos(time) * np.eye(dim, dtype=complex) - 1j * np.sin(time) * mat_P
    
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits[::-1]))
    
    return circuit
