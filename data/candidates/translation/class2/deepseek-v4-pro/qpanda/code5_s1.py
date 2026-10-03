# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QProg, X

def create_state_prep():
    prog = QProg()
    q = prog.qAllocMany(2)
    prog << X(q[0])
    return prog
