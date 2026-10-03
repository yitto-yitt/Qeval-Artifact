# EVAL_META: task_id=126, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def calculate_phase_difference_fidelity():
    # Create quantum machine and programs
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    
    # Create first operator (Hadamard gate)
    prog_a = pq.QProg()
    prog_a.insert(pq.H(qubits[0]))
    
    # Create second operator (Hadamard gate with global phase)
    prog_b = pq.QProg()
    prog_b.insert(pq.H(qubits[0]))
    
    # Get unitary matrices for both programs
    unitary_a = pq.get_unitary_matrix(prog_a, machine)
    unitary_b = pq.get_unitary_matrix(prog_b, machine)
    
    # Apply global phase to second operator
    unitary_b_with_phase = np.exp(1j * 0.5) * unitary_b
    
    # Calculate process fidelity
    # In pyQPanda3, we compute fidelity as |Tr(U1^dagger * U2)|^2 / d^2
    # where d is the dimension of the Hilbert space
    d = 2  # For single qubit system
    fidelity = abs(np.trace(unitary_a.conj().T @ unitary_b_with_phase))**2 / (d**2)
    
    machine.finalize()
    return fidelity
