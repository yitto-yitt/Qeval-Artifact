# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QOperator

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def compose_op():
    op = QOperator.Identity(3)
    yx = QOperator.Pauli("Y0 X1")
    return op.compose(yx, [0, 2], True)

machine.finalize()
