# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, U4
import numpy as np

def custom_rotation_gate():
    circuit = QCircuit(1)
    circuit << U4(np.pi / 2, np.pi / 2, np.pi / 2, 0.0, 0)
    return circuit
