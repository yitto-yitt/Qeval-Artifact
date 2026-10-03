# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, CNOT

def create_swap_gate():
    qvm = CPUQVM()
    qvm.init()
    q0 = qvm.qAlloc()
    q1 = qvm.qAlloc()

    prog = QProg()
    prog << CNOT(q0, q1)
    prog << CNOT(q1, q0)
    prog << CNOT(q0, q1)

    return prog
