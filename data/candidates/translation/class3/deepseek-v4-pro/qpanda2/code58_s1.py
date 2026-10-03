# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_ch_gate():
    prog = QProg()
    prog << RY(q[1], np.pi / 4) << CNOT(q[0], q[1]) << RY(q[1], -np.pi / 4)
    return prog

machine.finalize()
