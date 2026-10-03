# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np


def compose_op():
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    # Pauli "YX": Y on qubit 1, X on qubit 0 -> Y (x) X
    yx = np.kron(Y, X)

    # 3-qubit identity
    op = np.eye(2 ** 3, dtype=complex)

    # Build the 3-qubit embedding of YX on qargs [0, 2]:
    # qarg[0] -> label position 0 (X), qarg[1] -> label position 1 (Y)
    # So X acts on qubit 0, Y acts on qubit 2.
    # Full operator ordering (qubit2, qubit1, qubit0): Y (x) I (x) X
    yx_embedded = np.kron(np.kron(Y, I2), X)

    # compose front=True: result = op @ yx_embedded
    result = op @ yx_embedded
    return result
