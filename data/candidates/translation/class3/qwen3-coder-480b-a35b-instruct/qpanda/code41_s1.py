# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *
from pyqpanda3.utils import *


def compose_op():
    # Create 3-qubit identity operator
    op = np.eye(2**3)
    
    # Create Pauli YX operator (Y on qubit 0, X on qubit 1)
    # In Qiskit's Pauli("YX"), the leftmost character corresponds to qubit 0
    # So YX means Y on qubit 0 and X on qubit 1
    y_matrix = np.array([[0, -1j], [1j, 0]])  # Pauli Y
    x_matrix = np.array([[0, 1], [1, 0]])     # Pauli X
    yx = np.kron(y_matrix, x_matrix)
    
    # Compose YX with identity on qubits 0 and 2
    # This means we need to put YX on qubits 0 and 2, which requires expanding
    # YX acts on 2 qubits, but we want it to act on qubits 0 and 2 of a 3-qubit system
    # So we need to tensor with identity for qubit 1 in the middle
    yx_expanded = np.kron(np.kron(y_matrix, np.eye(2)), x_matrix)
    
    # In Qiskit's compose method with front=True, it's op.compose(yx, qargs=[0, 2], front=True)
    # This means apply yx first, then op
    # But since op is identity, the result is just yx expanded to the full space
    return Operator(yx_expanded)
