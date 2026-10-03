# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * cirq.unitary(cirq.H)

    # Process fidelity for unitary operators A and B is |Tr(A^\dagger B)|^2 / d^2
    dim = op_a.shape[0]
    fidelity = np.abs(np.trace(np.conjugate(op_a).T @ op_b)) ** 2 / (dim**2)
    return fidelity
