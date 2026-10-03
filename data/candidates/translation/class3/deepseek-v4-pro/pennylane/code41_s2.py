# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml

def compose_op():
    return qml.prod(qml.PauliY(0), qml.Identity(wires=1), qml.PauliX(2))
