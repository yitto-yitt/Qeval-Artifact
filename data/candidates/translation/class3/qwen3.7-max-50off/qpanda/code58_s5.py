# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, CNOT
import numpy as np

def create_ch_gate():
    cir = QCircuit()
    q = cir.qAlloc(2)
    cir << RY(q[1], np.pi/4)
    cir << CNOT(q[0], q[1])
    cir << RY(q[1], -np.pi/4)
    return cir
