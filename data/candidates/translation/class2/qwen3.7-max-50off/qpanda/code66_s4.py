# EVAL_META: task_id=66, framework=qpanda, class=2
import numpy as np
try:
    from pyqpanda3.core import QuantumCircuit
except ImportError:
    from pyqpanda3 import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3)
    qc.ry(2 * np.arccos(1 / np.sqrt(3)), 0)
    qc.ch(0, 1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.x(0)
    qc.measure_all()
    return qc
