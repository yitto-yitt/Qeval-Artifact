# EVAL_META: task_id=108, framework=qiskit, class=3
from qiskit.quantum_info import Choi

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint = choi1.adjoint()
    composed = choi1.compose(choi2)
    return choi1, adjoint, composed
