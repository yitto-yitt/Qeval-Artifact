# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np


def calculate_phase_difference_fidelity():
    H = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    d = op_a.shape[0]
    overlap = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(overlap / d) ** 2
    return fidelity
