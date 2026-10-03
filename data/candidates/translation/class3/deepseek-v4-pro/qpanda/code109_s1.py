# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3 import QProg, qalloc, H, RZ, Variation

def circuit():
    theta = Variation()
    q = qalloc()
    prog = QProg()
    prog << H(q) << RZ(theta, q)
    return prog
