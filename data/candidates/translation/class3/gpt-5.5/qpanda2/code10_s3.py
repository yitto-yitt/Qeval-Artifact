# EVAL_META: task_id=10, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)
atexit.register(machine.finalize)

def create_operator():
    prog = QProg()
    prog.insert(U3(q[0], math.pi, 0.0, math.pi))
    prog.insert(U3(q[1], math.pi, 0.0, math.pi))
    return prog
