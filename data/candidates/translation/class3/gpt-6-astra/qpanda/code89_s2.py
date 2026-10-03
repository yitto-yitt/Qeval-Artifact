# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QProg, H

def create_controlled_hgate():
    prog = QProg()
    prog << H(2).control([0, 1])
    return prog
