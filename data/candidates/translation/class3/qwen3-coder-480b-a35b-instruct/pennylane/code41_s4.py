# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def compose_op():
    # Create a 3-qubit identity operator
    identity_op = qml.Identity(wires=[0, 1, 2])
    
    # Create YX operator on qubits 0 and 2
    yx_op = qml.PauliY(wires=0) @ qml.PauliX(wires=2)
    
    # Compose the operators - apply YX to qubits 0 and 2 of the identity
    composed_op = qml.prod(identity_op, yx_op).simplify()
    
    return composed_op
