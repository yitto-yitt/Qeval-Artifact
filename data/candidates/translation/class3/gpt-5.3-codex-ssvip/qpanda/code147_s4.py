# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Y, control

def mcy(qc):
    controls = [qc[0], qc[1], qc[2], qc[3]]
    target = qc[4]
    qc << control(Y(target), controls)
    return qc
