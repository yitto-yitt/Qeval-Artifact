# EVAL_META: task_id=13, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, U3, qAlloc

def custom_rotation_gate():
    q = qAlloc()
    circuit = QCircuit()
    circuit << U3(q, np.pi / 2, np.pi / 2, np.pi / 2)
    return circuit
