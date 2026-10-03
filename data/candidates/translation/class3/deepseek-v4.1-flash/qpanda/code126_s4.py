# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, H, get_matrix

def calculate_phase_difference_fidelity():
    circuit = QCircuit()
    circuit << H(0)
    op_a = np.array(get_matrix(circuit))
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (d**2)
    return float(fidelity)
