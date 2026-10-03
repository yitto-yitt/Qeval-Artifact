# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import *

def create_c3sx_circuit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)
    prog = QProg()
    prog.insert(C3SX(q[0], q[1], q[2], q[3]))
    return prog
