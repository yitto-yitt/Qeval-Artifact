# EVAL_META: task_id=41, framework=cirq, class=3

import cirq


def compose_op():
    q0, q1, q2 = cirq.LineQubit.range(3)
    identity = cirq.PauliString()
    yx = cirq.PauliString({q0: cirq.Y, q2: cirq.X})
    return identity * yx
