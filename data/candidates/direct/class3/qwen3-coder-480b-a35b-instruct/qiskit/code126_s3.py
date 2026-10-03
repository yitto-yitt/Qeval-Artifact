# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np

def calculate_phase_difference_fidelity():
    # Create a quantum circuit with one qubit
    qc1 = QuantumCircuit(1)
    qc1.h(0)  # Apply Hadamard gate
    
    # Create another quantum circuit with one qubit
    # Apply Hadamard gate followed by a global phase change
    qc2 = QuantumCircuit(1)
    qc2.h(0)  # Apply Hadamard gate
    qc2.global_phase = np.pi / 2  # Add a global phase of pi/2 (equivalent to multiplying by i)

    # Convert circuits to operators
    op1 = Operator(qc1)
    op2 = Operator(qc2)
    
    # Calculate the process fidelity between the two operators
    fidelity = process_fidelity(op1, op2)
    
    return fidelity
