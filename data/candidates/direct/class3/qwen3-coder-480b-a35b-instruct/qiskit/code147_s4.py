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
    # For 5 qubits where qubits 0-3 control and qubit 4 is target
    
    # Method: Use a standard decomposition for multi-controlled Y
    # Y gate can be written as: Y = S * X * S.dag()
    # So MCY = MC(S) * MC(X) * MC(S.dag())
    
    # However, for a direct implementation, we can use the fact that:
    # Multi-controlled Y on controls [0,1,2,3] and target 4
    qc.cp(3.14159 / 2, 3, 4)  # Phase shift related to Y rotation
    qc.mcx([0, 1, 2], 4)       # Multi-controlled X with 3 controls
    qc.cp(-3.14159 / 2, 3, 4)  # Reverse phase shift
    qc.mcx([0, 1, 2], 4)       # Another multi-controlled X to complete the Y-like operation
    
    # Actually, let's implement the proper multi-controlled Y gate
    # Y = [[cos(pi/2), -sin(pi/2)], [sin(pi/2), cos(pi/2)]] = [[0, -1], [1, 0]]
    # This is just i*X up to a global phase, but we need the exact Y operation
    
    # Reset the circuit operations and implement correctly
    qc.data.clear()  # Clear previous operations
    
    # Implement multi-controlled Y gate properly
    # Y = SXS† where S = [[1,0],[0,i]], X = [[0,1],[1,0]], S† = [[1,0],[0,-i]]
    # So MCY = MC(S) * MC(X) * MC(S†)
    
    # Apply S† to target if all controls are 1
    qc.cp(-3.14159 / 2, 3, 4)  # Apply S† phase when control qubit 3 is 1
    qc.mcx([0, 1, 2], 3)       # Ancilla setup to check all controls
    qc.cp(-3.14159 / 2, 3, 4)  # Apply remaining S† phase when all controls are 1
    qc.mcx([0, 1, 2], 3)       # Undo ancilla setup
    
    # Apply X to target if all controls are 1
    qc.mcx([0, 1, 2, 3], 4)    # Multi-controlled X gate (all 4 controls)
    
    # Apply S to target if all controls are 1  
    qc.cp(3.14159 / 2, 3, 4)   # Apply S phase when control qubit 3 is 1
    qc.mcx([0, 1, 2], 3)       # Ancilla setup again
    qc.cp(3.14159 / 2, 3, 4)   # Apply remaining S phase when all controls are 1
    qc.mcx([0, 1, 2], 3)       # Undo ancilla setup
    
    # A simpler approach using existing methods
    qc.data.clear()  # Start fresh
    
    # The correct way: Using the equivalence Y = u3(pi, pi/2, pi/2)
    # For multi-controlled version, we apply the u3 angles conditionally
    from qiskit.circuit.library import MCXGate
    
    # Since Y gate is U3(pi, pi/2, pi/2), we need to implement this controlled
    # The most straightforward way is to use the built-in support or decompose manually
    
    # Use a standard decomposition: MCY can be implemented with auxiliary gates
    # Y = S * X * S.dag(), so MCY = MC-S * MC-X * MC-S.dag()
    
    # Apply MC(S.dag()) to qubit 4 controlled by qubits 0,1,2,3
    qc.cp(-3.14159/2, 0, 4)  # Controlled phase for S.dag part
    qc.cp(-3.14159/2, 1, 4)
    qc.cp(-3.14159/2, 2, 4)
    qc.cp(-3.14159/2, 3, 4)
    
    # Now add the multi-controlled X
    qc.mcx([0, 1, 2, 3], 4)
    
    # Apply MC(S) to qubit 4 controlled by qubits 0,1,2,3
    qc.cp(3.14159/2, 0, 4)  # Controlled phase for S part
    qc.cp(3.14159/2, 1, 4)
    qc.cp(3.14159/2, 2, 4)
    qc.cp(3.14159/2, 3, 4)
    
    return qc
