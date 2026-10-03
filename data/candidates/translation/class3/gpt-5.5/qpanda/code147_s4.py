# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    gate = Y(4).control([0, 1, 2, 3])
    result = qc << gate
    return qc if result is None else result
