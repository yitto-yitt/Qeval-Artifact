# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def bv_algorithm(s):
    n = len(s)
    
    dev = qml.device("default.qubit", wires=n+1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize ancilla to |1>
        qml.PauliX(wires=n)
        
        # Apply Hadamard to all qubits
        for i in range(n+1):
            qml.Hadamard(wires=i)
            
        # Apply CNOT gates based on secret string s
        for idx, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[idx, n])
                
        # Apply Hadamard to input qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
            
        # Measure input qubits
        return qml.sample(wires=range(n))
    
    bitstrings = [circuit()]
    result = {"samples": bitstrings}
    
    return [bitstrings, result]
