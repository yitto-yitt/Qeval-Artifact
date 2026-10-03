# EVAL_META: task_id=41, framework=pennylane, class=3
import pennylane as qml
from pennylane.operation import Tensor


def compose_op():
    return Tensor(qml.PauliY(0), qml.Identity(1), qml.PauliX(2))
