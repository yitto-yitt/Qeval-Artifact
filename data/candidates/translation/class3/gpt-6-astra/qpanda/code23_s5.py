# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QProg, X

def dj_constant_oracle():
    oracle = QProg()
    oracle << X(2)
    return oracle
