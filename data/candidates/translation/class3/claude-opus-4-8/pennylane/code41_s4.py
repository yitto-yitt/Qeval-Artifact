# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    # YX Pauli embedded on qubits [0, 2] of a 3-qubit system.
    # Qiskit ordering (q2 ⊗ q1 ⊗ q0): Y on qubit 2, I on qubit 1, X on qubit 0
    matrix = np.kron(Y, np.kron(I, X))
    return qml.QubitUnitary(matrix, wires=[2, 1, 0])
