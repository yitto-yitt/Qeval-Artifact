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
    
    # Initialize device with different initial states to get columns of unitary
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def apply_circuit_with_state(initial_state):
        qml.QubitStateVector(initial_state, wires=[0, 1])
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()
    
    # Compute unitary by applying to each computational basis state
    basis_states = [
        [1, 0, 0, 0],  # |00>
        [0, 1, 0, 0],  # |01>
        [0, 0, 1, 0],  # |10>
        [0, 0, 0, 1]   # |11>
    ]
    
    for i, state in enumerate(basis_states):
        result = apply_circuit_with_state(state)
        unitary[:, i] = result
    
    return unitary
