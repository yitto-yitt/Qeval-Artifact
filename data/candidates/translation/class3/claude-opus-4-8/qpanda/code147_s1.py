# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Y

def mcy(qc):
    y_gate = Y(4)
    y_gate.control([0, 1, 2, 3])
    qc << y_gate
    return qc
