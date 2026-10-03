# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import *

def create_operator():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = QProg()
    prog.insert(X(q[0]))
    prog.insert(X(q[1]))

    optimized_prog = circuit_optimizer(prog, machine, 1)
    return optimized_prog
