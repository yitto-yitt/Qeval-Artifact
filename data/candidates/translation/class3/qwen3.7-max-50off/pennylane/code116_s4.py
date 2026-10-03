# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
import numpy as np
from scipy.linalg import expm
from functools import reduce

def synthesize_evolution_gate(pauli_string, time):
    wires = list(range(len(pauli_string)))
    pauli_map = {
        'I': np.array([[1, 0], [0, 1]], dtype=complex),
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex)
    }
    
    mats = [pauli_map[p] for p in pauli_string]
    if len(mats) == 0:
        mat = np.array([[1]], dtype=complex)
    else:
        mat = reduce(np.kron, mats)
        
    U = expm(-1j * time * mat)
    
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(U, wires=wires)
        
    return tape
