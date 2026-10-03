# EVAL_META: task_id=13, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def custom_rotation_gate():
    prog = QProg()
    prog << U4(q[0], 0.0, np.pi / 2, np.pi / 2, np.pi / 2)
    return prog

machine.finalize()
