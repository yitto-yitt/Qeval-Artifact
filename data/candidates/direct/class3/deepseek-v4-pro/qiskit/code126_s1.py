# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np

def calculate_phase_difference_fidelity():
    # Hadamard matrix
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    # Create an operator with a global phase (e.g., e^{iπ} = -1)
    phase = np.exp(1j * np.pi)  # -1
    H_phased = H * phase
    op1 = Operator(H)
    op2 = Operator(H_phased)
    fid = process_fidelity(op1, op2)
    return fid
