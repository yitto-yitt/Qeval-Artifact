# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def get_unitary():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()
    
    # Get the unitary by computing the state after applying the circuit to computational basis states
    # |00> -> first column
    dev._state = np.array([1, 0, 0, 0], dtype=complex)
    col1 = circuit()
    
    # Reset device and prepare |01> -> second column
    dev._state = np.array([0, 1, 0, 0], dtype=complex)
    col2 = circuit()
    
    # Reset device and prepare |10> -> third column
    dev._state = np.array([0, 0, 1, 0], dtype=complex)
    col3 = circuit()
    
    # Reset device and prepare |11> -> fourth column
    dev._state = np.array([0, 0, 0, 1], dtype=complex)
    col4 = circuit()
    
    unitary = np.column_stack([col1, col2, col3, col4])
    return unitary
