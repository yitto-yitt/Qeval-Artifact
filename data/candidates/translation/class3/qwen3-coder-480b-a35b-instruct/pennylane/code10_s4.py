# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_operator():
    # Define the unitary matrix
    U = np.array([[0, 0, 0, 1], 
                  [0, 0, 1, 0], 
                  [0, 1, 0, 0], 
                  [1, 0, 0, 0]])
    
    # Create a device with 2 qubits
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=[0, 1])
        return qml.state()
    
    # We need to decompose the unitary into basic gates (single-qubit + CNOT)
    # The given unitary is equivalent to swapping the |00> and |11> states while keeping |01> and |10>
    # This can be achieved by applying X gates on both qubits followed by a SWAP-like operation
    # Actually, looking at the matrix, it's a bit flip on both qubits followed by a swap
    
    # Let's build the operator explicitly
    def decomp_circuit():
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 0])
        qml.CNOT(wires=[0, 1])
    
    return decomp_circuit
