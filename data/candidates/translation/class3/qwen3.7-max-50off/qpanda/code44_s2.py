# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, X, CRY

def tensor_circuits():
    q = Qubit(3)
    prog = QProg()
    prog << CRY(0.2, q[0], q[1])
    prog << X(q[2])
    return prog
