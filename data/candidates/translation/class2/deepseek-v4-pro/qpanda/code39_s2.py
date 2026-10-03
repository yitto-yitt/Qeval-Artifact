# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import init_qvm, finalize_qvm, qAlloc_many, QProg, H, getQState

def create_uniform_superposition(n):
    init_qvm()
    try:
        q = qAlloc_many(n)
        prog = QProg()
        for i in range(n):
            prog << H(q[i])
        return getQState(prog, q)
    finally:
        finalize_qvm()
