# EVAL_META: task_id=41, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
def compose_op():
    prog = QProg()
    prog << X(q[0]) << Y(q[2])
    return get_unitary_matrix(prog)
machine.finalize()
