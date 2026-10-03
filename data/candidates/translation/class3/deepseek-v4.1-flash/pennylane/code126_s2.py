# EVAL_META: task_id=126, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def calculate_phase_difference_fidelity():
    op_a = qml.Hadamard(wires=0)
    op_b = qml.s_prod(np.exp(1j * 0.5), qml.Hadamard(wires=0))

    mat_a = qml.matrix(op_a)
    mat_b = qml.matrix(op_b)

    d = mat_a.shape[0]
    fidelity = np.abs(np.trace(np.conj(mat_a.T) @ mat_b) / d) ** 2
    return fidelity
