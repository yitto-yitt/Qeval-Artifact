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
            qubits,
            n_moments=np.random.randint(5, 20),  # Random number of moments
            op_density=0.8
        )
        
        # Get the unitary of the random circuit
        random_unitary = random_circuit.unitary()
        
        # Check equivalence up to global phase within tolerance
        # Using the condition that |tr(U1^\dagger U2)| should be close to |tr(I)| = dimension
        trace_overlap = abs(np.trace(original_unitary.conj().T @ random_unitary))
        expected_trace = abs(np.trace(np.eye(len(original_unitary))))
        
        # Check if they are equivalent within tolerance
        if abs(trace_overlap - expected_trace) <= 0.4 * expected_trace:
            equivalent_circuits.append(random_circuit)
            counter += 1
            
    return equivalent_circuits
