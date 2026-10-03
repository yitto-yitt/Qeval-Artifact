# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import init, finalize, QAlloc, QProg, H, statevector_run

def create_uniform_superposition(n):
    init()
    q = QAlloc(n)
    prog = QProg()
    for i in range(n):
        prog << H(q[i])
    sv = statevector_run(prog)
    finalize()
    return sv
