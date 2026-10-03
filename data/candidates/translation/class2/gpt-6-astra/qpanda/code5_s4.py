# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QProg, X, I


def create_state_prep():
    prog = QProg()
    prog << X(0) << I(1)
    return prog
