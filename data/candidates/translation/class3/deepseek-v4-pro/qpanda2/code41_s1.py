# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import CPUQVM, PauliOperator

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def compose_op():
    return PauliOperator("Y0 X2", 1.0)


machine.finalize()
