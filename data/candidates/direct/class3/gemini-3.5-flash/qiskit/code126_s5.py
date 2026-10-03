# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.quantum_info import Operator, process_fidelity
from qiskit.circuit.library import HGate

def calculate_phase_difference_fidelity():
    # Create Hadamard operator
    op1 = Operator(HGate())
    # Create another operator with a global phase difference (e.g., e^{i * pi / 4})
    op2 = np.exp(1j * np.pi / 4) * op1
    # Calculate process fidelity between the two operators
    fidelity = process_fidelity(op1, op2)
    return fidelity
