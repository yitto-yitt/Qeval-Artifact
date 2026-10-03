# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, CX
import numpy as np

def create_ch_gate():
    circ = QCircuit()
    circ << RY(1, np.pi/4)
    circ << CX(0, 1)
    circ << RY(1, -np.pi/4)
    return circ
