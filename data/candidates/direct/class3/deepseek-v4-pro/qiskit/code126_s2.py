# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity


def calculate_phase_difference_fidelity():
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    op1 = Operator(h)
    op2 = Operator(np.exp(1j * np.pi / 4) * h)
    return process_fidelity(op1, target=op2)
