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
    
    # To get the unitary, we need to construct it by applying the circuit to basis states
    # |00>, |01>, |10>, |11>
    unitary = np.zeros((4, 4), dtype=complex)
    
    # Reset device and apply operations for each computational basis state
    dev.reset()
    
    @qml.qnode(dev)
    def prepare_and_run(state_prep_ops):
        if state_prep_ops[0] == 1:
            qml.PauliX(wires=0)
        if state_prep_ops[1] == 1:
            qml.PauliX(wires=1)
            
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()
    
    # Compute columns of the unitary matrix
    for i in range(4):
        # Reset the device
        dev.reset()
        # Prepare the i-th computational basis state (binary representation)
        binary_state = [int(b) for b in format(i, '02b')]
        # Reverse order to match wire ordering (wire 0 is least significant bit)
        binary_state = [binary_state[1], binary_state[0]]
        
        col = prepare_and_run(binary_state)
        unitary[:, i] = col
    
    return unitary
