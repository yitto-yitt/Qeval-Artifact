# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import *

def create_ghz(drawing=False):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    for i in range(3):
        prog << Measure(q[i], c[i])

    if drawing:
        draw_text = draw_qprog_text(prog, machine)
        return prog, draw_text
    return prog
