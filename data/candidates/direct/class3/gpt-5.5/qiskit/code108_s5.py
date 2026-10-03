# EVAL_META: task_id=108, framework=qiskit, class=3
from qiskit.quantum_info import Choi


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint1 = choi1.adjoint()
    composed12 = choi1.compose(choi2)
    composed21 = choi2.compose(choi1)
    return choi1, adjoint1, composed12, composed21
