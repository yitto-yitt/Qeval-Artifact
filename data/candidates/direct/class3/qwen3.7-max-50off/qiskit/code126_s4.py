# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.quantum_info import Operator, process_fidelity
from qiskit.circuit.library import HGate
import numpy as np

def calculate_phase_difference_fidelity():
    h_mat = HGate().to_matrix()
    op1 = Operator(h_mat)
    op2 = Operator(np.exp(1j * np.pi / 4) * h_mat)
    return process_fidelity(op1, op2)
