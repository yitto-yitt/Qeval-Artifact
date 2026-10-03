# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    init(QMachineType.CPU)
    q = qAlloc()
    prog = QProg()
    prog << U3(q, np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
