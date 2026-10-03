# EVAL_META: task_id=126, framework=cirq, class=3
import numpy as np
import cirq


def calculate_phase_difference_fidelity():
    # Create Hadamard gate as a unitary matrix
    H = cirq.unitary(cirq.H)
    
    # Create two operators that differ by a global phase
    op_a = cirq.KrausChannel([H])
    op_b = cirq.KrausChannel([np.exp(1j * 0.5) * H])
    
    # Convert to superoperators for process fidelity calculation
    super_op_a = cirq.kraus_to_superoperator(op_a.kraus_ops)
    super_op_b = cirq.kraus_to_superoperator(op_b.kraus_ops)
    
    # Calculate process fidelity
    fidelity = np.real(np.trace(super_op_a.conj().T @ super_op_b) / len(super_op_a))
    
    return fidelity
