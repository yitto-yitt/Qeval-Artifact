# EVAL_META: task_id=126, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    qc1 = QuantumCircuit(1)
    qc1.h(0)

    qc2 = QuantumCircuit(1)
    qc2.h(0)
    qc2.global_phase = np.pi / 3

    op1 = Operator(qc1)
    op2 = Operator(qc2)

    return process_fidelity(op1, op2)
