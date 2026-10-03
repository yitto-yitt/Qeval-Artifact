# EVAL_META: task_id=60, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(2)

def create_cy_gate():
    prog = QProg()
    prog << U1(q[1], -math.pi / 2)
    prog << CNOT(q[0], q[1])
    prog << U1(q[1], math.pi / 2)
    return prog

machine.finalize()
