# EVAL_META: task_id=52, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np


def send_bits(bitstring):
    dev = qml.device('default.qubit', wires=2, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Create Bell state (entanglement between sender and receiver)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        
        qml.Barrier()
        
        # Apply Pauli corrections based on the bitstring
        if bitstring[1] == "1":
            qml.PauliZ(wires=0)
        if bitstring[0] == "1":
            qml.PauliX(wires=0)
            
        qml.Barrier()
        
        # Perform Bell measurement
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        
        # Measure both qubits
        return qml.sample(wires=[0, 1])
    
    # Execute the circuit
    result = circuit()
    
    # Convert sample to binary string format
    if dev.shots == 1:
        # For single shot, result is a 1D array
        measurement = ''.join([str(int(bit)) for bit in result])
    else:
        # For multiple shots, take the first result
        measurement = ''.join([str(int(bit)) for bit in result[0]])
    
    return measurement
