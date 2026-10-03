# EVAL_META: task_id=126, framework=qiskit, class=3
from qiskit.quantum_info import Operator
from qiskit.circuit.library import HGate
import numpy as np

def calculate_phase_difference_fidelity():
    # Create the first operator using Hadamard gate
    h_gate = HGate()
    op1 = Operator(h_gate)
    
    # Create the second operator by adding a global phase of π (phase of -1)
    # This is equivalent to multiplying the entire matrix by -1
    op2_matrix = -op1.data
    op2 = Operator(op2_matrix)
    
    # Calculate the process fidelity between the two operators
    from qiskit.quantum_info import process_fidelity
    fidelity = process_fidelity(op1, op2)
    
    return fidelity
