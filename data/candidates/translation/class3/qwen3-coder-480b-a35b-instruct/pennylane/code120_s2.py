# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    # Calculate number of qubits needed based on diagonal size
    num_qubits = int(np.log2(len(diag)))
    
    def circuit():
        # Apply diagonal operation using QubitUnitary
        # Construct the diagonal matrix
        diag_matrix = np.diag(diag)
        # Reshape to match expected dimensions for QubitUnitary
        qml.QubitUnitary(diag_matrix, wires=range(num_qubits))
    
    # Create a device with enough qubits
    dev = qml.device('default.qubit', wires=num_qubits)
    
    # Convert the circuit function to a QNode
    qnode = qml.QNode(circuit, dev)
    
    return qnode
