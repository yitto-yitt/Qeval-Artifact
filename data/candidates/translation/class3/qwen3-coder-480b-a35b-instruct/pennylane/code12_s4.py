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
    
    # To get the unitary, we need to compute the evolution for each basis state
    # |00>, |01>, |10>, |11>
    unitary = np.zeros((4, 4), dtype=complex)
    
    # Initialize device with |00> state
    dev._state = np.zeros(4, dtype=complex)
    dev._state[0] = 1.0
    
    # Apply the circuit to each computational basis state
    for i in range(4):
        # Reset the state to the i-th computational basis state
        initial_state = np.zeros(4, dtype=complex)
        initial_state[i] = 1.0
        dev._state = initial_state
        
        # Execute the circuit
        circuit()
        
        # The final state is the i-th column of the unitary matrix
        unitary[:, i] = dev._state
    
    return unitary
