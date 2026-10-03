# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit
import numpy as np

def custom_rotation_gate():
    qc = QuantumCircuit(1)
    qc.u3(np.pi / 2, np.pi / 2, np.pi / 2, 0)
    return qc
