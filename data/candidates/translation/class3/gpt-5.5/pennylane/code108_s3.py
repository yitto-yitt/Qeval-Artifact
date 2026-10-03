# EVAL_META: task_id=108, framework=pennylane, class=3
import math
import pennylane as qml
from pennylane import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.array(data1, dtype=complex)
    choi2 = np.array(data2, dtype=complex)

    n1 = choi1.shape[0]
    n2 = choi2.shape[0]
    d1 = math.isqrt(n1)
    d2 = math.isqrt(n2)

    if d1 * d1 != n1 or d2 * d2 != n2:
        raise ValueError("Choi matrix dimensions must be perfect squares.")

    choi1_4 = np.reshape(choi1, (d1, d1, d1, d1))
    adjoint_choi1 = np.reshape(np.transpose(np.conjugate(choi1_4), (1, 0, 3, 2)), choi1.shape)

    composed_4 = np.einsum(
        "ambn,minj->aibj",
        np.reshape(choi1, (d1, d1, d1, d1)),
        np.reshape(choi2, (d2, d2, d2, d2)),
    )
    composed_choi = np.reshape(composed_4, choi1.shape)

    return choi1, adjoint_choi1, composed_choi
