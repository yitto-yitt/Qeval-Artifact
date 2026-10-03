# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda3.core import QCircuit, matrix_decompose, QMatrix

def synthesize_evolution_gate(pauli_string, time):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    paulis = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    mat = None
    for ch in pauli_string:
        p = paulis[ch]
        mat = p if mat is None else np.kron(mat, p)

    U = expm(-1j * time * mat)

    n = len(pauli_string)
    qubits = list(range(n))
    qmat = QMatrix(U)
    circuit = matrix_decompose(qubits, qmat)
    return circuit
