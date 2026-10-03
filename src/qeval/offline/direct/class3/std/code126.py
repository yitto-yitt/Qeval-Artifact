# EVAL_META: task_id=126, framework=qiskit, class=3

import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity


def calculate_phase_difference_fidelity():
    op_a = Operator(HGate())
    op_b = np.exp(1j * 0.5) * Operator(HGate())
    fidelity = process_fidelity(op_a, op_b)
    return fidelity


# ==================================================
