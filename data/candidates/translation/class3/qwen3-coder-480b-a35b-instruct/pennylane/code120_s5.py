# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    # Calculate number of qubits needed based on diagonal size
    num_qubits = int(np.log2(len(diag)))
    
    # Create a quantum device
    dev = qml.device('default.qubit', wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        # Apply diagonal operation using QubitUnitary
        # Create the diagonal matrix
        diag_matrix = np.diag(diag)
        # Reshape to match expected dimensions for QubitUnitary
        qml.QubitUnitary(diag_matrix, wires=list(range(num_qubits)))
        return qml.state()
    
    # We need to return the operations that make up the circuit
    # Since PennyLane doesn't have a direct Diagonal gate, we use QubitUnitary
    def build_circuit():
        diag_matrix = np.diag(diag)
        qml.QubitUnitary(diag_matrix, wires=list(range(int(np.log2(len(diag))))))
    
    return build_circuit
