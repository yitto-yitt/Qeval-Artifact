# EVAL_META: task_id=12, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)


def get_unitary():
    prog = QProg()
    prog << H(q[1]) << CNOT(q[1], q[0])
    mat = get_matrix(prog)
    return np.array(mat).reshape(4, 4)


machine.finalize()
