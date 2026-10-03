# EVAL_META: task_id=4, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    matrix = np.array(matrix, dtype=complex)
    
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(matrix, wires=[0, 1])
        return qml.state()
    
    # We need to return the operation itself, not the qnode
    # Create a tape to hold the operation
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(matrix, wires=[0, 1])
    
    return tape
