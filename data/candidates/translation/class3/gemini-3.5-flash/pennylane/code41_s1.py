# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml


def compose_op():
    return qml.X(0) @ qml.Y(2)
