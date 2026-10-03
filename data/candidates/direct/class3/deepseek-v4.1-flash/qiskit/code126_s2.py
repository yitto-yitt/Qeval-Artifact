# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    op1 = Operator(HGate())
    op2 = Operator(HGate()) * np.exp(1j * np.pi / 4)
    return process_fidelity(op1, op2)
