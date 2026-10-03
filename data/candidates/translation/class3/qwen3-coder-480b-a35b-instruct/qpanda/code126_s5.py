# EVAL_META: task_id=126, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def calculate_phase_difference_fidelity():
    # Create quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    
    # Create H gate as circuit A
    prog_a = pq.QProg()
    prog_a.insert(pq.H(qubits[0]))
    
    # Get unitary matrix for H gate
    unitary_a = pq.get_unitary(prog_a, qubits)
    
    # Create H gate again as circuit B (same operation)
    prog_b = pq.QProg()
    prog_b.insert(pq.H(qubits[0]))
    
    # Get unitary matrix for H gate
    unitary_b = pq.get_unitary(prog_b, qubits)
    
    # Apply global phase to second operator
    unitary_b_with_phase = np.exp(1j * 0.5) * unitary_b
    
    # Calculate process fidelity using the unitary matrices
    # For single-qubit gates, process fidelity can be computed as |Tr(U1^dagger U2)|^2 / d^2
    # where d is dimension (2 for single qubit)
    d = 2
    fidelity = abs(np.trace(unitary_a.conj().T @ unitary_b_with_phase))**2 / (d**2)
    
    return fidelity
