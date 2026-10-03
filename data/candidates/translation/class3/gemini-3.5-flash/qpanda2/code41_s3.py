# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def compose_op():
    # Y on qubit 2, X on qubit 0
    op = PauliOperator({"Y2 X0": 1.0})
    return op


# Manual Cleanup
machine.finalize()
