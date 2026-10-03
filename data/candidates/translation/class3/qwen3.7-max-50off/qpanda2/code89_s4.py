# EVAL_META: task_id=89, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QProg, RY, Toffoli

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = QProg()
    prog << RY(q[2], np.pi/4)
    prog << Toffoli(q[0], q[1], q[2])
    prog << RY(q[2], -np.pi/4)
    return prog

machine.finalize()
