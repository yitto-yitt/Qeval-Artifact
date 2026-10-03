# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    # Pauli("YX"): qubit0=X, qubit1=Y; composed on qargs [0,2] of 3-qubit identity
    # system qubit0=X, qubit1=I, qubit2=Y -> matrix = Y (x) I (x) X (little-endian)
    mat = np.kron(Y, np.kron(I, X))
    return qml.QubitUnitary(mat, wires=[0, 1, 2])
