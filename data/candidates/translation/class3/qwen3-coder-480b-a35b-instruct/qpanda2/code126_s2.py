# EVAL_META: task_id=126, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    # Create quantum programs for both operators
    prog_a = pq.QProg()
    prog_b = pq.QProg()
    
    # Apply Hadamard gate to both
    prog_a << pq.H(qubits[0])
    prog_b << pq.H(qubits[0])
    
    # Get unitary matrices
    op_a = pq.get_unitary_matrix(prog_a, qubits)
    op_b = pq.get_unitary_matrix(prog_b, qubits)
    
    # Apply global phase to second operator
    op_b = np.exp(1j * 0.5) * op_b
    
    # Calculate process fidelity manually since pyqpanda doesn't have built-in process_fidelity
    # Process fidelity formula: F_process = |Tr(U1^\dagger U2)|^2 / d^2
    # where d is dimension of the operator
    d = op_a.shape[0]
    trace_value = np.trace(np.conj(op_a.T) @ op_b)
    fidelity = np.abs(trace_value)**2 / (d**2)
    
    return fidelity

result = calculate_phase_difference_fidelity()
machine.finalize()
