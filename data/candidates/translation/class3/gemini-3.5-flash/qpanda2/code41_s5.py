# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def compose_op():
    op = PauliOperator({"Y2 X0": 1.0})
    return op


machine.finalize()
