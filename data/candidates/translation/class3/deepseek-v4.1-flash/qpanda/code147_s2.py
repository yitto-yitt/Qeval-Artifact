# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QGate

def mcy(qc):
    qc << QGate("Y", 4).control([0, 1, 2, 3])
    return qc
