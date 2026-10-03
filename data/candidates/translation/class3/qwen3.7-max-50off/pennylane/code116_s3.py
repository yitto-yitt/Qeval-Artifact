# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    wires = list(range(n_qubits))
    
    mat = np.eye(1, dtype=complex)
    for p in pauli_string:
        if p == 'I':
            mat = np.kron(mat, np.eye(2, dtype=complex))
        elif p == 'X':
            mat = np.kron(mat, np.array([[0, 1], [1, 0]], dtype=complex))
        elif p == 'Y':
            mat = np.kron(mat, np.array([[0, -1j], [1j, 0]], dtype=complex))
        elif p == 'Z':
            mat = np.kron(mat, np.array([[1, 0], [0, -1]], dtype=complex))
            
    U = expm(-1j * time * mat)
    
    with qml.queuing.AnnotatedQueue() as q:
        qml.QubitUnitary(U, wires=wires)
        
    return qml.tape.QuantumScript.from_queue(q)
