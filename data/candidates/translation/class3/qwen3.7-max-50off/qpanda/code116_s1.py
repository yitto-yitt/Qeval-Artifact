# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
import scipy.linalg
from pyqpanda3.core import QCircuit, QGate

def synthesize_evolution_gate(pauli_string, time):
    paulis = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    mat = np.array([[1]], dtype=complex)
    for p in pauli_string:
        mat = np.kron(mat, paulis[p])
        
    U = scipy.linalg.expm(-1j * time * mat)
    
    qc = QCircuit()
    gate = QGate(U)
    qc << gate
    
    return qc
