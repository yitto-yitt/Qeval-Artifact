# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize the last qubit to |1⟩
        qml.PauliX(wires=n-1)
        
        # Apply Hadamard to all qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply the oracle
        oracle.decomposition()
        
        # Apply Hadamard to all qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the first n-1 qubits
        return qml.probs(wires=range(n-1))
    
    probs = circuit()
    # Create a dictionary with bitstring keys and their probabilities
    num_bits = n - 1
    prob_dict = {}
    for i in range(2**num_bits):
        bitstring = format(i, f'0{num_bits}b')
        prob_dict[bitstring] = probs[i]
    
    return prob_dict
