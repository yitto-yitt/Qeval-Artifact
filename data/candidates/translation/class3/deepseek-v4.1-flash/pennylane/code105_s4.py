# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def initialize_cnot_dihedral():
    U = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, np.exp(1j * np.pi / 4)],
        [0, 0, np.exp(1j * np.pi / 4), 0]
    ], dtype=complex)
    return qml.QubitUnitary(U, wires=[0, 1])
