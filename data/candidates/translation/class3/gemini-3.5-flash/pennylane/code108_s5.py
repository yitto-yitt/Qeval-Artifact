# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.math.asarray(data1)
    choi2 = qml.math.asarray(data2)

    # Compute adjoint of choi1
    sh1 = qml.math.shape(choi1)
    d2_1 = sh1[0]
    d_1 = int(qml.math.sqrt(d2_1))
    tensor1 = qml.math.reshape(choi1, (d_1, d_1, d_1, d_1))
    adj_tensor = qml.math.transpose(tensor1, (1, 0, 3, 2))
    adj_tensor = qml.math.conj(adj_tensor)
    adjoint_choi1 = qml.math.reshape(adj_tensor, (d2_1, d2_1))

    # Compute composition: choi1.compose(choi2) -> choi1 after choi2
    sh2 = qml.math.shape(choi2)
    d2_2 = sh2[0]
    d_2 = int(qml.math.sqrt(d2_2))

    J_first = qml.math.reshape(choi2, (d_2, d_2, d_2, d_2))
    J_second = qml.math.reshape(choi1, (d_1, d_1, d_1, d_1))

    # Contract output of J_first (axes 1, 3) with input of J_second (axes 0, 2)
    R = qml.math.tensordot(J_first, J_second, axes=((1, 3), (0, 2)))
    # R has axes (i, j, a, b). Transpose to (i, a, j, b)
    composed_tensor = qml.math.transpose(R, (0, 2, 1, 3))
    composed_choi = qml.math.reshape(composed_tensor, (d2_1, d2_1))

    return choi1, adjoint_choi1, composed_choi
