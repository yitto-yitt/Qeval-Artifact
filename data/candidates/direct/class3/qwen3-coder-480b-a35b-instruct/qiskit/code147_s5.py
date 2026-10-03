# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit


def mcy(qc):
    """
    Adds a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3.
    
    Args:
        qc (QuantumCircuit): The quantum circuit to apply the operation to
        
    Returns:
        QuantumCircuit: The modified quantum circuit
    """
    # Apply multi-controlled Y gate using a sequence of operations
    # We'll use the fact that Y = RZ(pi/2) * X * RZ(-pi/2)
    # But more directly, we can use a decomposition with CNOTs and single-qubit gates
    
    # First, decompose Y in terms of known gates: Y = S * X * S†
    # So MCY = MC(S * X * S†) = MC(S) * MCX * MC(S†)
    
    # We'll implement this using ancilla-free method with a series of Toffoli gates
    # For 4 control qubits, we need to decompose into Toffoli gates and single-qubit rotations
    
    # Create a temporary ancilla-based implementation if needed
    # But for direct implementation, we can use Qiskit's built-in support or manual decomposition
    
    # Use the standard decomposition for multi-controlled Y gate
    # Y gate can be written as: Y = U3(π, π/2, π/2)
    
    # Implementation using decomposition
    # Using the fact that Y = SXS† where S = sqrt(Z)
    qc.s(4)  # Apply S to target qubit
    qc.mcx([0, 1, 2, 3], 4)  # Multi-controlled X gate
    qc.sdg(4)  # Apply S† to target qubit
    
    return qc
