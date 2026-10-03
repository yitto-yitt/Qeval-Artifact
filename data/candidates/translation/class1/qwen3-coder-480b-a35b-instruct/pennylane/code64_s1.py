# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    dev = qml.device('default.qubit', wires=n*2)
    
    @qml.qnode(dev)
    def circuit():
        # Apply Hadamard gates to first n qubits
        for i in range(n):
            qml.Hadamard(wires=i)
        
        qml.Barrier()
        
        # Apply CX gates between corresponding qubits
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
        # If there's a '1' in s, apply additional CX gates
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n+j])
            
            qml.Barrier()
            
            # Apply Hadamard gates to first n qubits again
            for k in range(n):
                qml.Hadamard(wires=k)
        
        # Measure first n qubits
        return [qml.measure(wires=i) for i in range(n)]
    
    # Execute the circuit
    result = circuit()
    
    # Create a quantum tape to represent the circuit
    return circuit.qtape
