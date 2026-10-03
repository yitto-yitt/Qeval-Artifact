# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def get_unitary():
    return qml.matrix(
        qml.prod(
            qml.CNOT(wires=[0, 1]),
            qml.Hadamard(wires=0),
        ),
        wire_order=[0, 1],
    )
