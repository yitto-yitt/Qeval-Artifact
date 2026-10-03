# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, get_unitary


def calculate_phase_difference_fidelity():
    q = [0]
    circ = QCircuit()
    circ << H(q[0])
    op_a = get_unitary(circ)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(op_a).T @ op_b))**2 / d**2
    return fidelity
