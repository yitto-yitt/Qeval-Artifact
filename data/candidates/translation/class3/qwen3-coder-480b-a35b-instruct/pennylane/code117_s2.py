# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    # Create a device to get the decomposition
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Decompose the unitary using Pennylane's template
        qml.QubitUnitary(unitary, wires=[0, 1])
        return qml.state()
    
    # Extract the operations by creating a tape
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(unitary, wires=[0, 1])
    
    # For a 4x4 unitary on 2 qubits, we need to decompose it
    # Using the decomposition available in pennylane
    decomp_ops = qml.transforms.decompositions.unitary_decomposition(tape.operations[0], wires=[0, 1])
    
    # Create a new tape with decomposed operations
    with qml.tape.QuantumTape() as new_tape:
        for op in decomp_ops:
            qml.apply(op)
    
    return new_tape.operations
