# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3 import QProg, H, CX, alloc_qubits

def apply_op_back():
    q = alloc_qubits(3)
    prog = QProg()
    prog << H(q[0])
    prog << CX(q[0], q[1])
    prog << H(q[0])
    return prog
