# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity
def calculate_phase_difference_fidelity():
    op1 = Operator(HGate())
    phase = np.pi / 2
    op2 = Operator(np.exp(1j * phase) * op1.data)
    fidelity = process_fidelity(op1, op2)
    return fidelity
