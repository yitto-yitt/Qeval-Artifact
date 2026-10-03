# EVAL_META: task_id=108, framework=cirq, class=3
from cirq.quantum_info import Superoperator


def initialize_adjoint_and_compose(data1, data2):
    choi1 = Superoperator.from_choi(data1)
    choi2 = Superoperator.from_choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
