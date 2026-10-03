# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog = QProg()
    prog << U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    qvm.finalize()
    return prog
