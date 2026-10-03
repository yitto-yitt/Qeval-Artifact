# EVAL_META: task_id=66, framework=qpanda, class=2
from math import acos, sqrt
from pyqpanda3.core import *

def w_state():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    prog.insert(RY(q[0], 2 * acos(1 / sqrt(3))))
    prog.insert(CH(q[0], q[1]))
    prog.insert(CNOT(q[1], q[2]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(X(q[0]))
    prog.insert(Measure(q[0], c[0]))
    prog.insert(Measure(q[1], c[1]))
    prog.insert(Measure(q[2], c[2]))

    return prog
