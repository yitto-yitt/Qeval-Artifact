# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    h = HGate()
    op1 = Operator(h)
    op2 = Operator(np.exp(1j * np.pi / 4) * h.to_matrix())
    return float(np.round(np.real(process_fidelity(op1, op2)), 12))
