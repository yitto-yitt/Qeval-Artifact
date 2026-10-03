# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumCircuit

def calculate_phase_difference_fidelity():
    qc_a = QuantumCircuit(1)
    qc_a.h(0)
    
    if hasattr(qc_a, 'matrix'):
        mat_a = qc_a.matrix()
    elif hasattr(qc_a, 'get_matrix'):
        mat_a = qc_a.get_matrix()
    else:
        mat_a = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
    mat_b = mat_a * np.exp(1j * 0.5)
    
    d = mat_a.shape[0]
    fidelity = np.abs(np.trace(mat_a.conj().T @ mat_b))**2 / (d**2)
    return float(fidelity)
