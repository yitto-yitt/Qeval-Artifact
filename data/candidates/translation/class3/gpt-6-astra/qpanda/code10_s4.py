# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, X

def create_operator():
    prog = QProg()
    prog << X(0) << X(1)
    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
