# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)

def create_ch_gate():
    prog = QProg()
    prog.insert(RY(q[1], pi/4))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(RY(q[1], -pi/4))
    return prog

machine.finalize()
