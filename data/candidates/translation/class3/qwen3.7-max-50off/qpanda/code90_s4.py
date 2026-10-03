# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QProg, X, H, qalloc

def create_custom_controlled():
    q = qalloc(4)
    prog = QProg()
    prog << X(q[1]).control([q[0], q[3]])
    prog << H(q[2]).control([q[0], q[3]])
    return prog
