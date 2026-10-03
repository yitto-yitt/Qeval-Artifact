# EVAL_META: task_id=4, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]])
    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(matrix, wires=[0, 1])
    return tape
