# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *

def custom_rotation_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    prog = QProg()
    prog.insert(U3(q[0], 1.5707963267948966, 1.5707963267948966, 1.5707963267948966))
    return prog
