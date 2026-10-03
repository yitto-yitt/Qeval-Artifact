# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    op = cirq.MatrixGate(np.eye(2**3, dtype=complex))
    yx = cirq.MatrixGate(np.kron(cirq.unitary(cirq.Y), cirq.unitary(cirq.X)))
    matrix = np.kron(np.kron(cirq.unitary(cirq.Y), np.eye(2, dtype=complex)), cirq.unitary(cirq.X))
    return cirq.MatrixGate(matrix)
