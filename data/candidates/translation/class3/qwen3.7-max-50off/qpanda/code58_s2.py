# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RY, CNOT
import numpy as np

def create_ch_gate():
    q0 = Qubit()
    q1 = Qubit()
    circ = QCircuit()
    circ << RY(q1, np.pi/4) << CNOT(q0, q1) << RY(q1, -np.pi/4)
    return circ
