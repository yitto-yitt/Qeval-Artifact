# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Qubit

def apply_op_back():
    q = [Qubit() for _ in range(3)]
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << H(q[0])
    return prog
