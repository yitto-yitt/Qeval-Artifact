# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity


def calculate_phase_difference_fidelity():
    h = Operator.from_label("H")
    h_phase = Operator(np.exp(1j * np.pi / 3) * h.data)
    return process_fidelity(h, h_phase)
