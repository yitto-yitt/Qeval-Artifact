# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, U3
import numpy as np

def custom_rotation_gate():
    circuit = QCircuit()
    q = Qubit(0)
    circuit << U3(np.pi / 2, np.pi / 2, np.pi / 2, q)
    return circuit
