# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Qubit

def apply_op_back():
    q = [Qubit(i) for i in range(3)]
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return prog
