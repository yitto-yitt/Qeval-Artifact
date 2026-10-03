# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import H


def calculate_phase_difference_fidelity():
    gate = H(0)
    for name in ("get_matrix", "matrix", "getMatrix"):
        if hasattr(gate, name):
            matrix = getattr(gate, name)
            matrix = matrix() if callable(matrix) else matrix
            op_a = np.asarray(matrix, dtype=complex).reshape(2, 2)
            break
    else:
        raise RuntimeError("The framework does not expose the Hadamard gate matrix.")

    op_b = np.exp(1j * 0.5) * op_a
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / 4
    return float(fidelity)
