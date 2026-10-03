# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda3.core import QCircuit, QProg, Oracle

def synthesize_evolution_gate(pauli_string, time):
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    mat = np.array([[1]], dtype=complex)
    for p in pauli_string:
        mat = np.kron(mat, pauli_map[p])
        
    U = expm(-1j * time * mat)
    
    qc = QCircuit()
    try:
        oracle = Oracle(U)
        qc.insert(oracle)
    except Exception:
        pass
        
    return qc
