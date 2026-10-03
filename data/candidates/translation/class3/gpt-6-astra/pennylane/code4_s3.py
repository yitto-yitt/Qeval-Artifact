# EVAL_META: task_id=4, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=complex,
    )
    with qml.tape.QuantumTape() as circuit:
        qml.QubitUnitary(matrix, wires=[1, 0])
    return circuit
