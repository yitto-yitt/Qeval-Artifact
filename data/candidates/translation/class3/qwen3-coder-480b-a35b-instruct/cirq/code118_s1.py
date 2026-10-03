# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    
    # Implementing C3SX gate using CNOT and T gates
    # C3SX is a triple-controlled SX gate
    # We'll build it using ancilla-based decomposition
    
    # First, create ancilla qubits for the decomposition
    ancilla1 = cirq.NamedQubit('ancilla1')
    ancilla2 = cirq.NamedQubit('ancilla2')
    
    # For simplicity, we'll use a direct approach with controlled operations
    # C3SX can be decomposed as a series of Toffoli gates and single-qubit rotations
    
    # However, since we need to match the exact behavior, let's construct it properly
    # Using the standard decomposition of a 3-controlled SX gate
    
    # Add the actual C3SX implementation
    # We'll use the fact that SX = sqrt(X) and build the controlled version
    
    # For a clean implementation without ancillas, we use multi-controlled operations
    circuit.append([
        cirq.X(qubits[3])**0.5,  # Apply SX (sqrt-X) to target
        cirq.CNOT(qubits[2], qubits[3]),  # Control from qubit 2
        cirq.X(qubits[3])**-0.5,
        cirq.CNOT(qubits[1], qubits[3]),  # Control from qubit 1
        cirq.X(qubits[3])**0.5,
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.X(qubits[3])**-0.5,
        cirq.CNOT(qubits[0], qubits[3]),  # Control from qubit 0
        cirq.X(qubits[3])**0.5,
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.X(qubits[3])**-0.5,
        cirq.CNOT(qubits[1], qubits[3]),
        cirq.X(qubits[3])**0.5,
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.X(qubits[3])**-0.5,
        cirq.CNOT(qubits[0], qubits[3]),
    ])
    
    # Truncate to only the first 4 qubits as required
    return circuit[:4]
