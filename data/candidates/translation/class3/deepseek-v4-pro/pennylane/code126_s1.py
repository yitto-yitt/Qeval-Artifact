# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def calculate_phase_difference_fidelity():
    op_a = qml.Hadamard.compute_matrix()
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(op_a).T @ op_b))**2 / (d**2)
    return fidelity
