# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    h_gate = cirq.H
    op_a = cirq.unitary(h_gate)
    op_b = np.exp(1j * 0.5) * cirq.unitary(h_gate)
    
    # Convert to superoperators for process fidelity calculation
    kraus_a = [op_a]
    kraus_b = [op_b]
    
    # Calculate process fidelity using the formula:
    # F_process = (1/d^2) * |Tr(U_a^\dagger U_b)|^2
    d = 2  # dimension of single qubit
    fidelity = abs(np.trace(np.conj(op_a.T) @ op_b))**2 / d**2
    
    return fidelity
