# EVAL_META: task_id=4, framework=pennylane, class=3
import pennylane as qml

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1],
              [0, 0, 1, 0],
              [1, 0, 0, 0],
              [0, 1, 0, 0]]
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(matrix, wires=[0, 1])
        return qml.state()

    return circuit
