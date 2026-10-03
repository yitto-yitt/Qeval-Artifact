# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
from collections import Counter


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
        return qml.sample(wires=list(range(n)))
    
    bitstrings = [tuple(circuit())]
    result = {"bitstrings": bitstrings}
    
    return [bitstrings, result]
