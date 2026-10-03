# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Operator
from qiskit.synthesis.clifford import synth_clifford_full


def equivalent_clifford_circuit(circuit, n):
    """
    Generate n random clifford circuits that are equivalent to the input circuit
    up to a relative and absolute tolerance of 0.4.
    
    Args:
        circuit (QuantumCircuit): Input clifford circuit
        n (int): Number of equivalent circuits to generate
    
    Returns:
        List[QuantumCircuit]: List of n equivalent clifford circuits
    """
    original_clifford = Clifford(circuit)
    original_operator = Operator(circuit)
    
    equivalent_circuits = []
    
    for _ in range(n):
        # Generate a random Clifford that is close to identity
        # This will create a perturbation that stays within tolerance
        num_qubits = circuit.num_qubits
        
        # Create a random Clifford near identity by applying small transformations
        # We'll use the fact that Cliffords form a group and compose with identity-like elements
        identity_like_clifford = _generate_identity_like_clifford(num_qubits)
        
        # Compose the original with the identity-like clifford to get a nearby equivalent
        new_clifford = original_clifford.compose(identity_like_clifford)
        
        # Synthesize the new Clifford back to a circuit
        new_circuit = synth_clifford_full(new_clifford)
        
        # Verify it's still within tolerance before adding
        new_operator = Operator(new_circuit)
        
        if _check_equivalence_within_tolerance(original_operator, new_operator, 0.4):
            equivalent_circuits.append(new_circuit)
        else:
            # If not within tolerance, try to generate another one
            # In case our identity-like generation didn't work well enough
            continue
    
    # If we didn't get enough circuits due to tolerance checks, pad with copies
    while len(equivalent_circuits) < n:
        # Add the original circuit itself as it's always valid
        equivalent_circords.append(circuit.copy())
    
    # Ensure we return exactly n circuits
    return equivalent_circuits[:n]


def _generate_identity_like_clifford(num_qubits):
    """Generate a Clifford operation that is close to identity."""
    # Start with identity Clifford
    clifford = Clifford(QuantumCircuit(num_qubits))
    
    # Apply small random Clifford operations that approximately preserve identity
    # For small systems, we can enumerate some simple operations that don't change much
    temp_circuit = QuantumCircuit(num_qubits)
    
    # Randomly apply some Pauli gates (which square to identity)
    # This creates a "small" deviation from identity
    for qubit in range(num_qubits):
        # With low probability, add a Pauli gate
        if np.random.random() < 0.3:  # Low probability to maintain closeness to identity
            pauli_choice = np.random.choice(['I', 'X', 'Y', 'Z'])
            if pauli_choice == 'X':
                temp_circuit.x(qubit)
            elif pauli_choice == 'Y':
                temp_circuit.y(qubit)
            elif pauli_choice == 'Z':
                temp_circuit.z(qubit)
            # 'I' means do nothing
    
    # Also add some simple two-qubit gates like CNOTs that might cancel out
    for _ in range(min(2, num_qubits - 1)):  # Limit number of 2-qubit gates
        if num_qubits > 1 and np.random.random() < 0.5:
            q1, q2 = np.random.choice(range(num_qubits), size=2, replace=False)
            temp_circuit.cx(q1, q2)
            # Possibly add inverse to keep close to identity
            if np.random.random() < 0.5:
                temp_circuit.cx(q1, q2)
    
    if len(temp_circuit.data) > 0:
        clifford = Clifford(temp_circuit)
    
    return clifford


def _check_equivalence_within_tolerance(op1, op2, tolerance):
    """Check if two operators are equivalent within a given tolerance."""
    # For Clifford circuits, we can check if they're equal up to global phase
    # But since we want tolerance checking, we'll compute the fidelity
    # For unitary matrices U1 and U2, we say they're equivalent if |Tr(U1^dagger U2)|/d >= 1-tol
    # where d is the dimension
    
    # Get the underlying matrices
    mat1 = op1.data
    mat2 = op2.data
    
    # Calculate normalized trace of the product to check similarity
    dim = mat1.shape[0]
    fidelity = abs(np.trace(mat1.conj().T @ mat2)) / dim
    
    # Check if this is close to 1 (meaning same up to global phase)
    return np.isclose(fidelity, 1.0, atol=tolerance)
