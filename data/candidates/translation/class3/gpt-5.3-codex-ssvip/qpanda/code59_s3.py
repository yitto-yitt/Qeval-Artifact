# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, qalloc_many

def create_cz_gate():
    q = qalloc_many(2)
    prog = QProg()
    prog << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return prog
