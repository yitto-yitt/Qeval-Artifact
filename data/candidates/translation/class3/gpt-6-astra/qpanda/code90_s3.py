# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QProg, X, H

def create_custom_controlled():
    prog = QProg()
    prog << X(1).control([0, 3])
    prog << H(2).control([0, 3])
    return prog
