# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, qAlloc_many, cAlloc_many, H, CNOT, Measure
from pyqpanda3.core import draw_qprog

def create_ghz(drawing=False):
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])
    if drawing:
        fig = draw_qprog(prog)
        return prog, fig
    return prog
