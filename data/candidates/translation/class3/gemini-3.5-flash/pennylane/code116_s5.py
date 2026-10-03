# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
import scipy.linalg

def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        'I': np.eye(2, dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    H = paulis[pauli_string[0]]
    for char in pauli_string[1:]:
        H = np.kron(H, paulis[char])
        
    U = scipy.linalg.expm(-1j * time * H)
    return qml.QubitUnitary(U, wires=list(range(len(pauli_string))))
