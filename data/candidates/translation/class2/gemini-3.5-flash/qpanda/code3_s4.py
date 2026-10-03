# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import *


def create_ghz(drawing=False):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(3)
    c = machine.cAllocMany(3)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])

    if drawing:
        return prog, draw_qprog(prog, "pic")
    return prog
