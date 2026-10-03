# EVAL_META: task_id=108, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def initialize_adjoint_and_compose(data1, data2):
    choi1 = data1
    choi2 = data2
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
machine.finalize()
