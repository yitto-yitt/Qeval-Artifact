# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def bv_algorithm(s):
    n = len(s)
    
    dev = qml.device("default.qubit", wires=n+1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize ancilla qubit to |1>
        qml.PauliX(wires=n)
        
        # Apply Hadamard to all qubits
        for i in range(n+1):
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates based on the secret string s
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        
        # Apply Hadamard to input qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the input qubits
        return qml.sample(wires=range(n))
    
    bitstrings = circuit()
    # Convert the sample to the expected format (list of strings)
    bitstring = ''.join(str(int(b)) for b in bitstrings)
    result = {"samples": [bitstring]}
    
    return [[bitstring], result]
