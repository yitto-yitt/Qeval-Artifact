# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    h_gate = cirq.H
    op_a = cirq.unitary(h_gate)
    op_b = np.exp(1j * 0.5) * cirq.unitary(h_gate)
    
    # Calculate process fidelity using the formula for unitary operators
    # Process fidelity between two unitary operators U1 and U2 is |Tr(U1^dagger U2)|^2 / d^2
    # where d is the dimension of the operator
    d = op_a.shape[0]
    overlap = np.trace(np.conj(op_a.T) @ op_b)
    fidelity = np.abs(overlap)**2 / (d**2)
    
    return fidelity
