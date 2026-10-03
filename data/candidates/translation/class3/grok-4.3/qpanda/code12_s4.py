# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import *

def get_unitary():
    prog = QProg()
    q = qAlloc_many(2)
    prog << H(q[0]) << CNOT(q[0], q[1])
    return get_unitary_matrix(prog)
