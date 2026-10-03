# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_bell_statevector():
    # Create a device with 2 qubits to work with the statevector
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare |00> state
        qml.PauliX(wires=0)  # Start with |10>
        qml.PauliX(wires=1)  # Change to |11>
        qml.PauliX(wires=0)  # Change to |01>
        qml.PauliX(wires=1)  # Back to |00>
        
        # Apply Hadamard to first qubit
        qml.Hadamard(wires=0)
        # Apply CNOT with control on first qubit, target on second
        qml.CNOT(wires=[0, 1])
        
        return qml.state()
    
    statevector = circuit()
    return statevector
