# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    # 3-qubit identity composed (front) with Pauli("YX") on qargs [0, 2].
    # Pauli("YX"): qubit0 -> X, qubit1 -> Y ; mapped to system qubits 0 and 2.
    # Qiskit ordering (qubit2 msb): kron(Y_q2, I_q1, X_q0)
    mat = np.kron(Y, np.kron(I, X))

    return qml.QubitUnitary(mat, wires=[0, 1, 2])
