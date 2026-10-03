# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QProg, QVec, H, CNOT

def simple_elitzur_vaidman():
    q = QVec(2)
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    return prog
