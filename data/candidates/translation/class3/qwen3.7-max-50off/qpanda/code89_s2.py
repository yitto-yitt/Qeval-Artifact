# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QProg, QVec, H

def create_controlled_hgate():
    qv = QVec(3)
    prog = QProg()
    prog << H(qv[2]).control([qv[0], qv[1]])
    return prog
