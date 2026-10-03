# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    paulis = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    mat = np.array([[1]], dtype=complex)
    for char in pauli_string:
        mat = np.kron(mat, paulis[char])
    U = expm(-1j * time * mat)
    return qml.tape.QuantumScript([qml.QubitUnitary(U, wires=list(range(n)))])
