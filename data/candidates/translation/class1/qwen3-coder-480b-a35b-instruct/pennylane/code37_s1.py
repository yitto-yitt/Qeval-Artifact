# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np


def bv_algorithm(s):
    n = len(s)
    
    dev = qml.device("default.qubit", wires=n+1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare ancilla qubit in |-> state
        qml.PauliX(wires=n)
        qml.Hadamard(wires=n)
        
        # Apply Hadamard to all input qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply oracle: CNOT gates for each '1' bit in s
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        
        # Apply Hadamard to all input qubits again
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure all input qubits
        return [qml.measure(wires=i) for i in range(n)]
    
    # Run the circuit
    result = circuit()
    
    # Convert results to bitstring (reverse order to match Qiskit convention)
    bitstring = "".join(str(int(r)) for r in reversed(result))
    
    return [[bitstring], circuit]
