# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.math.asarray(data1)
    choi2 = qml.math.asarray(data2)
    adjoint_choi1 = qml.math.conj(qml.math.transpose(choi1))
    dim = int(np.sqrt(qml.math.shape(choi1)[0]))
    choi1_reshaped = qml.math.reshape(choi1, (dim, dim, dim, dim))
    choi2_reshaped = qml.math.reshape(choi2, (dim, dim, dim, dim))
    composed_reshaped = qml.math.einsum("abmn,mncd->abcd", choi1_reshaped, choi2_reshaped)
    composed_choi = qml.math.reshape(composed_reshaped, (dim * dim, dim * dim))
    return choi1, adjoint_choi1, composed_choi
