# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import init, qAlloc_many, H, CNOT, QProg

_initialized = False

def apply_op_back():
    global _initialized
    if not _initialized:
        init()
        _initialized = True
    q = qAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return prog
