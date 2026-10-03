# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    # Create Hadamard operator
    op1 = Operator.from_label('H')
    # Create Hadamard operator with a global phase
    op2 = np.exp(1j * np.pi / 4) * op1
    # Calculate process fidelity
    fidelity = process_fidelity(op1, op2)
    return fidelity
