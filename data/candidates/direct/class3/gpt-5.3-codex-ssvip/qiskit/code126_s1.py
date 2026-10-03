# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity


def calculate_phase_difference_fidelity():
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    op1 = Operator(qc1)

    qc2 = QuantumCircuit(1)
    qc2.global_phase = 0.5  # pi * 0.5 = pi/2 global phase
    qc2.h(0)
    op2 = Operator(qc2)

    return process_fidelity(op1, op2)
