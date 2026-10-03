# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()


def compose_op():
    return PauliOperator({"Y2 X0": 1.0})


machine.finalize()
