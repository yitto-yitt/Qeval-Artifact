# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml
import numpy as np


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    # Create device with 2n qubits (equivalent to two n-qubit registers)
    dev = qml.device('default.qubit', wires=2*n)
    
    @qml.qnode(dev)
    def circuit():
        # Apply Hadamard to first n qubits (reg1)
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates between reg1 and reg2
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
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
    
    # Execute the circuit to get samples
    samples = circuit()
    
    # We need to return a quantum circuit object, but PennyLane doesn't have the same 
    # circuit representation as Qiskit. Instead we'll create a template function
    # that represents the operations that would be performed
    
    def apply_simon_circuit(wires):
        # First n wires are reg1, next n wires are reg2
        reg1_wires = wires[:n]
        reg2_wires = wires[n:]
        
        # Apply Hadamard to first n qubits (reg1)
        for i in reg1_wires:
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates between reg1 and reg2
        for i, j in zip(reg1_wires, reg2_wires):
            qml.CNOT(wires=[i, j])
        
        if "1" in s:
            i_idx = s.find("1")
            control_wire = reg1_wires[i_idx]
            for j in range(n):
                if s[j] == "1":
                    target_wire = reg2_wires[j]
                    qml.CNOT(wires=[control_wire, target_wire])
            
            # Apply Hadamard again to first n qubits
            for i in reg1_wires:
                qml.Hadamard(wires=i)
        
        # For measurement, we return the operations
        measurements = []
        for i in reg1_wires:
            measurements.append(qml.sample(qml.PauliZ(wires=i)))
        
        return measurements
    
    # Create a new device with 2n wires
    device = qml.device('default.qubit', wires=2*n)
    
    # Define the qnode with our circuit
    @qml.qnode(device)
    def constructed_circuit():
        apply_simon_circuit(list(range(2*n)))
        return qml.probs(wires=list(range(n)))  # probabilities of measuring first n qubits
    
    # Return the constructed circuit function
    return apply_simon_circuit, constructed_circuit, device, list(range(2*n))
