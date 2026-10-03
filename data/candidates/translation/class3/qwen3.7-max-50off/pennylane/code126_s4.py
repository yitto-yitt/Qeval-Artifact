# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def calculate_phase_difference_fidelity():
    H = qml.Hadamard.compute_matrix()
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    
    d = op_a.shape[0]
    trace_val = np.trace(np.conj(op_a).T @ op_b)
    fidelity = np.abs(trace_val)**2 / (d**2)
    
    return float(fidelity)
