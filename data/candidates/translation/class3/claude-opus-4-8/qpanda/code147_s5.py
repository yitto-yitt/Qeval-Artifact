# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y

def mcy(qc):
    mcy_gate = Y(4).control([0, 1, 2, 3])
    qc << mcy_gate
    return qc
