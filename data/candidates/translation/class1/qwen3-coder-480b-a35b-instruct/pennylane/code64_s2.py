# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    # Create the device with n*2 qubits (equivalent to two n-qubit registers)
    dev = qml.device('default.qubit', wires=n*2)
    
    @qml.qnode(dev)
    def circuit():
        # Apply Hadamard to first n qubits (q_reg1 equivalent)
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates between corresponding qubits of first and second register
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
        # If there's a '1' in s, apply additional operations
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n+j])
            
            # Apply Hadamard again to first n qubits
            for i in range(n):
                qml.Hadamard(wires=i)
        
        # Measure the first n qubits
        return [qml.sample(qml.PauliZ(i)) for i in range(n)]
    
    # Actually create a QNode that we can run
    # Since PennyLane doesn't have explicit classical registers like Qiskit,
    # we need to return a representation of the circuit structure
    # Let's build the tape directly
    
    tape = qml.transforms.make_tape(circuit)()
    
    # We'll create a QNode with the operations
    def qnode_function():
        # Apply Hadamard to first n qubits (q_reg1 equivalent)
        for i in range(n):
            qml.Hadamard(wires=i)
        
        qml.Barrier(wires=list(range(2*n)))
        
        # Apply CNOT gates between corresponding qubits of first and second register
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
        # If there's a '1' in s, apply additional operations
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n+j])
            
            qml.Barrier(wires=list(range(2*n)))
            
            # Apply Hadamard again to first n qubits
            for i in range(n):
                qml.Hadamard(wires=i)
        
        # Measure the first n qubits - return samples
        return [qml.sample(wires=i) for i in range(n)]
    
    # Return the quantum function that represents the circuit
    return qnode_function
