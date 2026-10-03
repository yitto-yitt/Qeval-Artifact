# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import Program, H, RZ, Parameter

def circuit():
    prog = Program()
    q = prog.qAlloc(1)
    theta = Parameter('th')
    prog << H(q[0]) << RZ(q[0], theta)
    return prog
