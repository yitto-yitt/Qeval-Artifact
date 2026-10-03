# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / d**2
    return fidelity
