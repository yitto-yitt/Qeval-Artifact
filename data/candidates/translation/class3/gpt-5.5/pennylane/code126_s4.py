# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def calculate_phase_difference_fidelity():
    op_a = qml.matrix(qml.Hadamard(wires=0))
    op_b = np.exp(1j * 0.5) * op_a
    dimension = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / (dimension ** 2)
    return float(np.real_if_close(fidelity))
