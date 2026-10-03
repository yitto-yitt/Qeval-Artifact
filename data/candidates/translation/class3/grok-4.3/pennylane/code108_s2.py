# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.math.array(data1)
    choi2 = qml.math.array(data2)
    adjoint_choi1 = qml.math.adjoint(choi1)
    composed_choi = qml.math.matmul(choi1, choi2)
    return choi1, adjoint_choi1, composed_choi
