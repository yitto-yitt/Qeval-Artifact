# EVAL_META: task_id=90, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def create_custom_controlled():
    x_matrix = np.array([[0, 1], [1, 0]], dtype=complex)
    h_matrix = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    custom_matrix = np.kron(x_matrix, h_matrix)

    op = qml.ControlledQubitUnitary(
        custom_matrix,
        control_wires=[0, 3],
        wires=[1, 2],
    )

    return qml.tape.QuantumScript(ops=[op], measurements=[])
