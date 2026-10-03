# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, process_fidelity

def calculate_phase_difference_fidelity():
    # Create first operator with Hadamard gate
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    op1 = Operator(qc1)
    
    # Create second operator with Hadamard gate and global phase
    qc2 = QuantumCircuit(1)
    qc2.h(0)
    qc2.global_phase = 3.14159 / 4  # Add a global phase
    op2 = Operator(qc2)
    
    # Calculate process fidelity
    fidelity = process_fidelity(op1, op2)
    
    return fidelity
