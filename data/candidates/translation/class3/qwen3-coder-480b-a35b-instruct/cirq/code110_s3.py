# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np
from cirq.transformers import random_clifford_circuit

def equivalent_clifford_circuit(circuit, n):
    # Convert input circuit to unitary matrix
    original_unitary = circuit.unitary()
    
    num_qubits = len(circuit.all_qubits())
    qubits = cirq.LineQubit.range(num_qubits)
    
    equivalent_circuits = []
    counter = 0
    
    while counter < n:
        # Generate a random Clifford circuit
        random_circuit = random_clifford_circuit(
            qubits=qubits,
            n_moments=np.random.randint(5, 20),  # Random number of moments
            op_density=0.8
        )
        
        # Get the unitary of the random circuit
        random_unitary = random_circuit.unitary()
        
        # Check equivalence within tolerance
        # Using the condition that ||U1 - U2||_F <= tol * sqrt(d) where d is dimension
        # Or check if |tr(U1^dag U2)|/d is close to 1 (for global phase consideration)
        diff_matrix = original_unitary - random_unitary
        frobenius_norm = np.linalg.norm(diff_matrix, 'fro')
        max_dim = np.sqrt(original_unitary.shape[0])
        
        # Alternative check for operator equivalence considering global phase
        trace_val = np.abs(np.trace(original_unitary.conj().T @ random_unitary)) / original_unitary.shape[0]
        is_equivalent = (frobenius_norm <= 0.4 * max_dim) or (np.abs(trace_val - 1) <= 0.4)
        
        if is_equivalent:
            counter += 1
            equivalent_circuits.append(random_circuit)
    
    return equivalent_circuits
