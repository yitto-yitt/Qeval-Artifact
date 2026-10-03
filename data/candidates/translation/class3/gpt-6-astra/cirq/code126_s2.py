# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * op_a
    dimension = op_a.shape[0]
    fidelity = np.abs(np.trace(op_b.conj().T @ op_a)) ** 2 / dimension**2
    return float(fidelity)
