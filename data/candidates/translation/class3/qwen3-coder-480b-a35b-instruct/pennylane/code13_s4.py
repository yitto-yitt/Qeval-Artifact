# EVAL_META: task_id=13, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def custom_rotation_gate():
    dev = qml.device('default.qubit', wires=1)
    
    @qml.qnode(dev)
    def circuit():
        qml.Rot(np.pi / 2, np.pi / 2, np.pi / 2, wires=0)
        return qml.expval(qml.PauliZ(0))
    
    # We need to return the operation, not execute it
    # Create a tape to capture the operations
    with qml.tape.QuantumTape() as tape:
        qml.Rot(np.pi / 2, np.pi / 2, np.pi / 2, wires=0)
    
    return tape.operations
