# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import Circuit, H

def calculate_phase_difference_fidelity():
    circ = Circuit(1)
    circ << H(0)
    
    H_mat = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    op_a = H_mat
    op_b = np.exp(1j * 0.5) * H_mat
    
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (d**2)
    
    return float(fidelity)
