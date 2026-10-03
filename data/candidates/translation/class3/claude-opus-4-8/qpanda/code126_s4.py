# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import H, QCircuit


def calculate_phase_difference_fidelity():
    circ = QCircuit(1)
    circ << H(0)
    op_a = circ.matrix()
    op_b = np.exp(1j * 0.5) * op_a

    d = op_a.shape[0]
    overlap = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(overlap / d) ** 2
    return fidelity
