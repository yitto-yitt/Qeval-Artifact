# EVAL_META: task_id=41, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def compose_op():
    eye = np.eye(2**3)
    op = qml.QubitUnitary(eye, wires=[0, 1, 2])

    yx = qml.matrix(qml.PauliY(0) @ qml.PauliX(1))

    yx_full = qml.matrix(
        qml.QubitUnitary(yx, wires=[0, 2]), wire_order=[0, 1, 2]
    )

    composed = qml.matrix(op, wire_order=[0, 1, 2]) @ yx_full
    return qml.QubitUnitary(composed, wires=[0, 1, 2])
