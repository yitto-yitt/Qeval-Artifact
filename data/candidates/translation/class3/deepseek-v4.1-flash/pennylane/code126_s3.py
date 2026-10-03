# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def calculate_phase_difference_fidelity():
    H = qml.matrix(qml.Hadamard(wires=0))
    op_a = H
    op_b = np.exp(1j * 0.5) * H
    d = op_a.shape[0]
    overlap = np.trace(np.conj(op_a.T) @ op_b)
    fidelity = np.abs(overlap) ** 2 / (d ** 2)
    return fidelity
