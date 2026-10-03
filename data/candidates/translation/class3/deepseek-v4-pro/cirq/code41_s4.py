# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    I_3 = np.eye(8, dtype=complex)
    yx = cirq.Y(0) * cirq.X(1)
    yx_mat = cirq.unitary(yx)
    yx_on_0_2 = cirq.unitary(
        cirq.identity(2) * cirq.identity(2)
    )
    yx_on_0_2 = np.kron(np.kron(cirq.unitary(cirq.Y), np.eye(2)), cirq.unitary(cirq.X)).reshape(8,8)
    op = I_3 @ yx_on_0_2
    return cirq.DenseMatrix(op)
