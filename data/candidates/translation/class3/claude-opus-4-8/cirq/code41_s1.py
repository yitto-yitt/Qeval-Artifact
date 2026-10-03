# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np


def compose_op():
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)

    yx = np.kron(Y, X)

    op = np.eye(2 ** 3, dtype=complex)

    # qargs=[0, 2]: Pauli "YX" applies Y to qubit 2, X to qubit 0
    # (Qiskit little-endian: leftmost Pauli char acts on last qarg)
    full = np.kron(Y, np.kron(I, X))

    result = full @ op
    return result
