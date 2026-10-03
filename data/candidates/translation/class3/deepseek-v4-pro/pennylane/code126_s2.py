# EVAL_META: task_id=126, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def calculate_phase_difference_fidelity():
    hadamard = qml.Hadamard(wires=0)
    op_a = qml.matrix(hadamard)
    op_b = np.exp(1j * 0.5) * op_a
    dim = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / dim ** 2
    return fidelity
