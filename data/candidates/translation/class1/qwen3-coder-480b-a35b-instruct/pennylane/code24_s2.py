# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize the last qubit to |1>
        qml.PauliX(wires=n-1)
        
        # Apply Hadamard to all qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply the oracle
        # Since oracle is a Qiskit circuit, we need to extract its operations
        # For this translation, we assume the oracle can be applied as a unitary
        # We'll use qml.QubitUnitary to apply the oracle if it's given as a matrix
        # Otherwise, we assume it's compatible with Pennylane operations
        
        # Convert Qiskit oracle to PennyLane operations
        # This requires extracting the unitary matrix from the oracle
        unitary_matrix = qml.matrix(oracle) if hasattr(oracle, 'to_matrix') else None
        if unitary_matrix is not None:
            qml.QubitUnitary(unitary_matrix, wires=list(range(n)))
        else:
            # If we cannot directly convert, we'll need to apply the oracle differently
            # Since we don't have access to internal operations, we'll create a custom operation
            qml.apply(oracle)
        
        # Apply Hadamard to all qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure all but the last qubit
        return qml.probs(wires=range(n-1))
    
    probs = circuit()
    
    # Convert probabilities to dictionary format
    result_dict = {}
    for i, prob in enumerate(probs):
        if prob > 1e-8:  # Only include non-negligible probabilities
            binary_str = format(i, f'0{n-1}b')
            result_dict[binary_str] = prob
    
    return result_dict
