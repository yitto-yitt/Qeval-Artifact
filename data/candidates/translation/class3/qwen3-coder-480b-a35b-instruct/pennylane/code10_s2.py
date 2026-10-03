# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    # Define the unitary matrix
    U = np.array([[0, 0, 0, 1], 
                  [0, 0, 1, 0], 
                  [0, 1, 0, 0], 
                  [1, 0, 0, 0]])
    
    # Create a QNode that implements the unitary
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=[0, 1])
        return qml.state()
    
    # Return the operation that represents the unitary
    return qml.QubitUnitary(U, wires=[0, 1])
