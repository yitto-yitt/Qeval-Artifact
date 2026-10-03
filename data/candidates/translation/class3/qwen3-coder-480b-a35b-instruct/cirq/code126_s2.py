# EVAL_META: task_id=126, framework=cirq, class=3
import cirq
import numpy as np


def calculate_phase_difference_fidelity():
    # Create Hadamard gate as a unitary operation
    h_gate = cirq.H
    qubit = cirq.LineQubit(0)
    
    # Get the unitary matrix for the Hadamard gate
    op_a_matrix = cirq.unitary(h_gate)
    
    # Create second operator with global phase difference
    global_phase = np.exp(1j * 0.5)
    op_b_matrix = global_phase * op_a_matrix
    
    # For process fidelity calculation in Cirq context, we need to compare the operations
    # Process fidelity between two unitaries differing by a global phase should be calculated
    # based on their action (which is the same up to global phase)
    
    # Since process fidelity measures how similar two quantum processes are,
    # and global phases don't affect the physical process, we calculate it accordingly
    # For single-qubit unitaries U1 and U2 = e^{i\phi}U1, process fidelity = 1
    # But let's compute it explicitly using the standard formula
    
    # Process fidelity formula: F_process = |Tr(U1^\dagger U2)|^2 / d^2
    # where d is the dimension of the Hilbert space
    d = 2  # Single qubit has dimension 2
    u1_dag_u2 = op_a_matrix.conj().T @ op_b_matrix
    trace_val = np.trace(u1_dag_u2)
    fidelity = np.abs(trace_val)**2 / (d**2)
    
    return fidelity
