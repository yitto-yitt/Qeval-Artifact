# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    q = qAlloc(1)
    prog = create_empty_qprog()
    theta = Parameter('th')
    prog << H(q) << RZ(q, theta)
    return prog
