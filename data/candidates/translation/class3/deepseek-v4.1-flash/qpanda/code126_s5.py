# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, get_matrix

def calculate_phase_difference_fidelity():
    circ = QCircuit()
    circ << H(0)
    prog = QProg()
    prog << circ
    mat_a = get_matrix(prog)
    mat_b = np.exp(1j * 0.5) * mat_a
    d = mat_a.shape[0]
    trace = np.trace(mat_a.conj().T @ mat_b)
    fidelity = (np.abs(trace) / d) ** 2
    return fidelity
