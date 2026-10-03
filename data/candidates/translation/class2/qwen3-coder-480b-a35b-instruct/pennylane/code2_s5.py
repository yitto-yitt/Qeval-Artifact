# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_bell_statevector():
    # Create a device with 2 qubits to work with the statevector
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def bell_circuit():
        # Prepare |00> state
        qml.PauliX(wires=0)  # Start with |10>
        qml.PauliX(wires=1)  # Then to |11>
        qml.PauliX(wires=0)  # Back to |01>
        qml.PauliX(wires=1)  # Back to |00>
        
        # Apply Hadamard to first qubit
        qml.Hadamard(wires=0)
        # Apply CNOT
        qml.CNOT(wires=[0, 1])
        
        return qml.state()
    
    state_vector = bell_circuit()
    return state_vector.reshape(-1)  # Reshape to match expected format
