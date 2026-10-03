# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np

def calculate_phase_difference_fidelity():
    # Create first operator with just a Hadamard gate
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    op1 = Operator(qc1)

    # Create second operator with Hadamard gate and a global phase difference
    qc2 = QuantumCircuit(1)
    qc2.u1(np.pi, 0)  # Add a global phase of π
    qc2.h(0)
    op2 = Operator(qc2)

    # Calculate process fidelity between the two operators
    fidelity = process_fidelity(op1, op2)
    
    return fidelity
