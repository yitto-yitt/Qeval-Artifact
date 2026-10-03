# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.QubitChannel(np.array(data1, dtype=complex), wires=[0])
    choi2 = qml.QubitChannel(np.array(data2, dtype=complex), wires=[0])

    choi1_matrix = qml.matrix(choi1)
    choi2_matrix = qml.matrix(choi2)

    adjoint_choi1 = np.conjugate(choi1_matrix).T
    composed_choi = choi1_matrix @ choi2_matrix

    return choi1_matrix, adjoint_choi1, composed_choi
