# EVAL_META: task_id=126, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def calculate_phase_difference_fidelity():
    # Create quantum machine and programs
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    
    # Create first operator (Hadamard)
    prog_a = pq.QProg()
    prog_a.insert(pq.H(qubits[0]))
    
    # Get unitary matrix for first operator
    unitary_a = pq.get_unitary(prog_a, qubits)
    
    # Create second operator (Hadamard with global phase)
    prog_b = pq.QProg()
    prog_b.insert(pq.H(qubits[0]))
    
    # Get unitary matrix for second operator
    unitary_b = pq.get_unitary(prog_b, qubits)
    
    # Apply global phase to second operator
    unitary_b_with_phase = np.exp(1j * 0.5) * unitary_b
    
    # Calculate process fidelity
    # Process fidelity between two unitaries U1 and U2 is |Tr(U1^dagger U2)|^2 / d^2
    # where d is the dimension
    d = unitary_a.shape[0]
    fidelity = abs(np.trace(unitary_a.conj().T @ unitary_b_with_phase))**2 / (d**2)
    
    machine.finalize()
    return fidelity
