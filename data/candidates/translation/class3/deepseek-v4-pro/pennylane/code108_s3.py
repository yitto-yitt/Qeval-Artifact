# EVAL_META: task_id=108, framework=pennylane, class=3
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = np.asarray(data1)
    choi2 = np.asarray(data2)

    adjoint_choi1 = choi1.conj().T

    d = int(np.sqrt(choi1.shape[0]))
    if d * d != choi1.shape[0]:
        raise ValueError("Choi matrix dimension must be a perfect square")

    c1 = choi1.reshape(d, d, d, d)
    c2 = choi2.reshape(d, d, d, d)

    s1 = np.transpose(c1, (1, 3, 0, 2)).reshape(d * d, d * d)
    s2 = np.transpose(c2, (1, 3, 0, 2)).reshape(d * d, d * d)

    s_composed = s1 @ s2

    c_composed = np.transpose(
        s_composed.reshape(d, d, d, d), (2, 0, 3, 1)
    ).reshape(d * d, d * d)

    return choi1, adjoint_choi1, c_composed
