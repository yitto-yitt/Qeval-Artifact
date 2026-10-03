# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, S


def create_c3sx_circuit():
    prog = QProg()
    prog << H(3)
    prog << S(3).control([0, 1, 2])
    prog << H(3)
    return prog
