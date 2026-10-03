# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_custom_controlled():
    X = np.array([[0, 1], [1, 0]])
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    custom_matrix = np.kron(X, H)
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.QubitUnitary(custom_matrix, wires=[1, 2]), control=[0, 3])
    return tape
