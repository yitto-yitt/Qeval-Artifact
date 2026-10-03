# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    def custom_unitary(params, wires):
        qml.Rot(*params, wires=wires)
    
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Define the custom unitary parameters
        params = [0.3, 0.2, 0.1]
        
        # Apply the controlled custom unitary
        qml.ctrl(custom_unitary, control=0)(params, wires=1)
        
        return qml.state()
    
    # We need to return the operation itself, not execute the circuit
    # Create a tape to capture the operations
    tape = qml.tape.QuantumTape()
    with tape:
        params = [0.3, 0.2, 0.1]
        qml.ctrl(custom_unitary, control=0)(params, wires=1)
    
    return tape
