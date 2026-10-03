# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    matrix = np.array([[1.0]])
    for char in pauli_string:
        matrix = np.kron(matrix, pauli_map[char])
    U = expm(-1j * time * matrix)
    return qml.tape.QuantumScript([qml.QubitUnitary(U, wires=range(n))])
