# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    h_gate = cirq.H
    op_a = cirq.unitary(h_gate)
    op_b = np.exp(1j * 0.5) * cirq.unitary(h_gate)
    
    # Convert to superoperator representation for process fidelity calculation
    def unitary_to_superop(u):
        d = u.shape[0]
        superop = np.kron(u.conj().T, u)
        return superop
    
    superop_a = unitary_to_superop(op_a)
    superop_b = unitary_to_superop(op_b)
    
    # Process fidelity for unitary channels
    fidelity = np.abs(np.trace(superop_a.conj().T @ superop_b)) / len(op_a)**2
    
    return fidelity
