# EVAL_META: task_id=12, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def get_unitary():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return np.array(get_matrix(prog))

machine.finalize()
