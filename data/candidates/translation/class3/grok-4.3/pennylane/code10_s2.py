# EVAL_META: task_id=10, framework=pennylane, class=3
import pennylane as qml

def create_operator():
    XX = qml.QubitUnitary([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], wires=[0, 1])
    return qml.decompose(XX)
