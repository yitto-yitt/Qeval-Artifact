# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def calculate_phase_difference_fidelity():
    U = qml.Hadamard.compute_matrix()
    V = np.exp(1j * 0.5) * U
    d = U.shape[0]
    fidelity = np.abs(np.trace(U.conj().T @ V))**2 / (d**2)
    return float(fidelity)
