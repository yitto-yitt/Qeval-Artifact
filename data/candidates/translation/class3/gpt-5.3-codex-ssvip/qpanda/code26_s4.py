# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import *

def bell_dag():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(Measure(q[0], c[0]))

    return prog
