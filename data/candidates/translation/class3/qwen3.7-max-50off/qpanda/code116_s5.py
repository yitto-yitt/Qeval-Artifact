# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda3 import QCircuit, QMachine

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qm = QMachine()
    q = qm.qAlloc_many(n)
    circ = QCircuit()
    
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    
    mat = np.array([[1]], dtype=complex)
    for p in reversed(pauli_string):
        if p == 'I': mat = np.kron(I, mat)
        elif p == 'X': mat = np.kron(X, mat)
        elif p == 'Y': mat = np.kron(Y, mat)
        elif p == 'Z': mat = np.kron(Z, mat)
        
    U = expm(-1j * time * mat)
    
    if hasattr(circ, 'unitary_matrix'):
        circ.unitary_matrix(q, U)
    elif hasattr(circ, 'unitary'):
        circ.unitary(q, U)
    else:
        from pyqpanda3.core import Gate
        circ.insert(Gate(U, q))
        
    return circ
