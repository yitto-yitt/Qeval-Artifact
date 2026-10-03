# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import Y

def mcy(qc):
    mcy_gate = Y().control([0, 1, 2, 3])
    qc.append(mcy_gate, [4])
    return qc
