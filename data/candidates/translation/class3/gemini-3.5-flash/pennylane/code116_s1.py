# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    
    matrices = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    H = matrices[pauli_string[0]]
    for char in pauli_string[1:]:
        H = np.kron(H, matrices[char])
        
    cos_t = np.cos(time)
    sin_t = np.sin(time)
    U = cos_t * np.eye(2**len(pauli_string)) - 1j * sin_t * H
    
    wires = list(range(len(pauli_string)))
    return qml.QubitUnitary(U, wires=wires)
