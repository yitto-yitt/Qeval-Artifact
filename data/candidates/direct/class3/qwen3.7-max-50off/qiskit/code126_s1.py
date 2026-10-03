# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.quantum_info import Operator, process_fidelity
from qiskit.circuit.library import HGate
import numpy as np

def calculate_phase_difference_fidelity():
    op1 = Operator(HGate())
    op2 = Operator(1j * op1.data)
    return process_fidelity(op1, op2)
