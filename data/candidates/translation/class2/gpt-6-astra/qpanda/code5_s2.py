# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, X


def create_state_prep():
    prog = QProg()
    prog << X(0) << X(1) << X(1)
    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
