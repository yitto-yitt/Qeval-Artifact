# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3 import QProg, H, CNOT, QVec

def apply_op_back():
    q = QVec(3)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    return prog
