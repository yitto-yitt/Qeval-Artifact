# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, RX


def create_parametrized_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog = QProg()
    theta = 0.0
    prog.insert(RX(q[0], theta))
    return prog
