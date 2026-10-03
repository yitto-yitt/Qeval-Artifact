# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumCircuit

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    mat = np.array([[1]], dtype=complex)
    for p in pauli_string:
        mat = np.kron(mat, pauli_map[p])
        
    dim = 2**n
    I_mat = np.eye(dim, dtype=complex)
    U = np.cos(time) * I_mat - 1j * np.sin(time) * mat
    
    qc = QuantumCircuit(n)
    qc.unitary(U, list(range(n)))
    return qc
