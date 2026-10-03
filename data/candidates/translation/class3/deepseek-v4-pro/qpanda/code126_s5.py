# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def calculate_phase_difference_fidelity():
    init()
    q = qAlloc_many(1)
    circ = QCircuit()
    circ << H(q[0])
    try:
        mat = get_matrix(circ, q)
    except Exception:
        mat = get_matrix(circ)
    op_a = np.asarray(mat, dtype=complex)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = float(np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (d * d))
    return fidelity
