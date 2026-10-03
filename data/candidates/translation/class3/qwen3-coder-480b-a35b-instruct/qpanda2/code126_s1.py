# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def calculate_phase_difference_fidelity():
    # Create quantum programs for both operators
    qubits_a = machine.qAlloc_many(1)
    prog_a = pq.QProg()
    
    # Apply Hadamard gate
    prog_a.insert(pq.H(qubits_a[0]))
    
    # Get unitary matrix for first operator
    unitary_a = pq.get_unitary_matrix(prog_a, machine)
    
    # Reset for second operator
    qubits_b = machine.qAlloc_many(1)
    prog_b = pq.QProg()
    
    # Apply Hadamard gate for second operator
    prog_b.insert(pq.H(qubits_b[0]))
    
    # Get unitary matrix for second operator
    unitary_b = pq.get_unitary_matrix(prog_b, machine)
    
    # Apply global phase difference to second operator
    phase_factor = np.exp(1j * 0.5)
    unitary_b_with_phase = phase_factor * unitary_b
    
    # Calculate process fidelity
    # In pyQPanda, we compute it manually as the absolute value squared of the trace
    # F = |Tr(U1^\dagger U2)|^2 / d^2 where d is dimension
    dim = unitary_a.shape[0]
    fidelity = abs(np.trace(np.conj(unitary_a.T) @ unitary_b_with_phase))**2 / (dim**2)
    
    # Free qubits
    machine.qFree_all()
    
    return fidelity

result = calculate_phase_difference_fidelity()
machine.finalize()
