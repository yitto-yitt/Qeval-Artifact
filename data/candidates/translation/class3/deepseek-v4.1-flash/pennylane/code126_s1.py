# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def calculate_phase_difference_fidelity():
    H = qml.Hadamard.compute_matrix()
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    d = 2
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / d**2
    return fidelity
