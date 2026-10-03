# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QProg, I, X

def dj_constant_oracle():
    oracle = QProg()
    oracle << I(0) << I(1) << X(2)
    return oracle
