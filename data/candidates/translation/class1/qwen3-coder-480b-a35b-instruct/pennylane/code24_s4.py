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
        oracle.decomposition()
        
        # Apply Hadamard to all qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the first n-1 qubits
        return qml.probs(wires=range(n-1))
    
    probs = circuit()
    
    # Convert probabilities to dictionary format
    result_dict = {}
    for i, prob in enumerate(probs):
        if not np.isclose(prob, 0.0):
            bitstring = format(i, f'0{n-1}b')
            result_dict[bitstring] = float(prob)
    
    return result_dict
