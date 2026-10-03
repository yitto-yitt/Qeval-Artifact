# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def calculate_phase_difference_fidelity():
    op_a = qml.matrix(qml.Hadamard(0))
    op_b = np.exp(1j * 0.5) * qml.matrix(qml.Hadamard(0))
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conjugate(op_a.T) @ op_b)) ** 2 / (d**2)
    return fidelity
