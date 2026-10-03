# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml


def compose_op():
    op = qml.Identity(wires=[2, 1, 0])
    yx = qml.prod(qml.PauliY(wires=2), qml.PauliX(wires=0))
    return qml.prod(op, yx)
