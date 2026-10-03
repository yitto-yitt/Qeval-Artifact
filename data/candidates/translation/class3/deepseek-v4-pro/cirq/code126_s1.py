# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq

def calculate_phase_difference_fidelity():
    op_a = cirq.unitary(cirq.H)
    op_b = np.exp(1j * 0.5) * op_a
    fidelity = cirq.fidelity(op_a, op_b)
    return float(fidelity)
