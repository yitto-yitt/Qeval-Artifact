# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def calculate_phase_difference_fidelity():
    # Create quantum programs for both operators
    prog_a = pq.QProg()
    prog_b = pq.QProg()
    
    # Apply Hadamard gate to both
    prog_a << pq.H(qubits[0])
    prog_b << pq.H(qubits[0])
    
    # Get unitary matrices
    unitary_a = pq.get_unitary(prog_a, machine)
    unitary_b = pq.get_unitary(prog_b, machine)
    
    # Add global phase to second operator (equivalent to multiplying by exp(1j*0.5))
    unitary_b = unitary_b * np.exp(1j * 0.5)
    
    # Calculate process fidelity manually since pyqpanda doesn't have built-in process_fidelity
    # Process fidelity between two unitaries U1 and U2 is |Tr(U1^\dagger U2)|^2 / d^2 where d is dimension
    d = unitary_a.shape[0]
    fidelity = abs(np.trace(unitary_a.conj().T @ unitary_b))**2 / (d**2)
    
    return fidelity

machine.finalize()
