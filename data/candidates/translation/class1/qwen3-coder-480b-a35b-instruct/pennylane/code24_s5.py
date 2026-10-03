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
        # For this implementation, we'll assume the oracle can be applied as a unitary
        # Convert oracle to a unitary matrix and apply it
        unitary_matrix = qml.matrix(oracle)
        qml.QubitUnitary(unitary_matrix, wires=list(range(n)))
        
        # Apply Hadamard to all qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the first n-1 qubits
        return qml.probs(wires=list(range(n-1)))
    
    probs = circuit()
    
    # Create a dictionary with bitstring keys and their probabilities
    result = {}
    for i, prob in enumerate(probs):
        if prob > 1e-8:  # Only include non-negligible probabilities
            bitstring = format(i, f'0{n-1}b')
            result[bitstring] = prob
    
    return result
