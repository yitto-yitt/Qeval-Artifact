# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    h_matrix = HGate().to_matrix()
    op1 = Operator(h_matrix)
    op2 = Operator(np.exp(1j * np.pi / 4) * h_matrix)
    return float(process_fidelity(op1, op2))
