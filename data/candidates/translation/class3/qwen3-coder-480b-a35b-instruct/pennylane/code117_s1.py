# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def decompose_unitary(unitary):
    # In PennyLane, we can use the template for two-qubit unitary decomposition
    # However, PennyLane doesn't have a direct equivalent to Qiskit's TwoQubitBasisDecomposer
    # We need to create a circuit that implements the given unitary
    
    # Create a device with 2 qubits
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        # Apply the unitary matrix directly using QubitUnitary
        qml.QubitUnitary(unitary, wires=[0, 1])
        return qml.state()
    
    # To get the operations that make up the decomposition,
    # we need to create a tape and extract the operations
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(unitary, wires=[0, 1])
    
    # Return the tape which contains the operations
    return tape
