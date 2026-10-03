# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    # Qiskit Pauli("YX") = Y (qubit1) ⊗ X (qubit0)
    yx = np.kron(Y, X)

    # Embed into 3-qubit space with yx acting on system qubits [0, 2]:
    # qubit2 -> Y, qubit1 -> I, qubit0 -> X  (Qiskit little-endian ordering)
    matrix = np.kron(Y, np.kron(I, X))

    # Composition with the 3-qubit identity (front=True) leaves the matrix unchanged.
    _ = np.eye(2 ** 3) @ matrix

    return qml.QubitUnitary(matrix, wires=[2, 1, 0])
