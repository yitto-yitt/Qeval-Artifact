# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def compose_op():
    # Create a 3-qubit identity operator
    identity_op = qml.Identity(wires=[0, 1, 2])
    
    # Create YX operator on qubits 0 and 2
    yx_op = qml.PauliY(wires=0) @ qml.PauliX(wires=2)
    
    # In PennyLane, we can represent the composed operator using tensor product
    # Since we want to compose YX with identity on specific qubits, we need to construct
    # the full operator appropriately
    
    # Create the full operator by taking tensor product
    full_op = qml.Identity(wires=1) @ yx_op
    
    # Convert to matrix form to match the behavior
    identity_matrix = qml.matrix(qml.Identity(wires=[0, 1, 2]))
    yx_matrix = qml.matrix(yx_op)(params={})
    
    # Reshape yx_matrix to act on all 3 qubits (with identity on wire 1)
    # We need to create the appropriate tensor structure
    y_on_0 = qml.matrix(qml.PauliY(wires=0))(params={})
    x_on_2 = qml.matrix(qml.PauliX(wires=2))(params={})
    id_on_1 = qml.matrix(qml.Identity(wires=1))(params={})
    
    # Tensor product: Y on qubit 0, I on qubit 1, X on qubit 2
    yix_matrix = np.kron(np.kron(y_on_0, id_on_1), x_on_2).reshape((8, 8))
    
    # Compose operation (equivalent to front=True in Qiskit means applying yx first then identity)
    # Since identity doesn't change anything, result is just yx acting on specified qubits
    composed_matrix = np.dot(identity_matrix, yix_matrix)
    
    # Create operator from the resulting matrix
    # In PennyLane, we'll return the tensor product representation
    return yx_op
