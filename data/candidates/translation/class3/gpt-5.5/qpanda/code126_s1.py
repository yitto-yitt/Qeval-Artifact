# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    op_a = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = abs(np.trace(np.conjugate(op_a.T) @ op_b)) ** 2 / (dim * dim)
    return float(np.real_if_close(fidelity))
