# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CX, Qubit

def apply_op_back():
    q0 = Qubit()
    q1 = Qubit()
    q2 = Qubit()
    prog = QProg()
    prog << H(q0)
    prog << CX(q0, q1)
    prog << H(q0)
    return prog
