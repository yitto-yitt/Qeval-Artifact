# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    circuit = QCircuit()
    q = qAlloc(1)
    circuit.insert(U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2))
    return circuit
