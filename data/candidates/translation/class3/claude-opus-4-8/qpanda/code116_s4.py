# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from scipy.linalg import expm
from pyqpanda3.core import QCircuit, matrix_decompose

def synthesize_evolution_gate(pauli_string, time):
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    paulis = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    op = None
    for ch in pauli_string:
        mat = paulis[ch]
        op = mat if op is None else np.kron(op, mat)

    U = expm(-1j * time * op)

    num_qubits = len(pauli_string)
    qubits = list(range(num_qubits))
    circuit = matrix_decompose(qubits, U)
    return circuit
