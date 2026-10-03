# EVAL_META: task_id=108, framework=pennylane, class=3
import pennylane as qml


def initialize_adjoint_and_compose(data1, data2):
    choi1 = qml.transforms.channel_matrix(data1)
    choi2 = qml.transforms.channel_matrix(data2)
    adjoint_choi1 = choi1.conj().T
    composed_choi = choi1 @ choi2
    return choi1, adjoint_choi1, composed_choi
