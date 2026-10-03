# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * cirq.unitary(cirq.H)
    d = op_a.shape[0]
    overlap = np.trace(op_a.conj().T @ op_b)
    fidelity = np.abs(overlap) ** 2 / d ** 2
    return fidelity
