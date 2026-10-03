# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import init, qAlloc, QProg, H, get_matrix, finalize


def calculate_phase_difference_fidelity():
    init()
    q = qAlloc()
    prog = QProg()
    prog << H(q)
    op_a = np.array(get_matrix(prog))
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = float(np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (d * d))
    finalize()
    return fidelity
