# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *


def get_unitary():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    u = get_unitary(prog)
    return np.array(u).reshape(4, 4)
