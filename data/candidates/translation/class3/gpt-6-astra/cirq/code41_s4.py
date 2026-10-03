# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    return cirq.MatrixGate(
        np.kron(
            cirq.unitary(cirq.Y),
            np.kron(np.eye(2, dtype=complex), cirq.unitary(cirq.X)),
        )
    )
