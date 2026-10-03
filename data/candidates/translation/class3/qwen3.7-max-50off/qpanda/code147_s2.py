# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    circ = QCircuit()
    circ.insert(Y(qc[4]).control([qc[0], qc[1], qc[2], qc[3]]))
    return circ
