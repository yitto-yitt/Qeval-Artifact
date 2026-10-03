# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np


def compose_op():
    q0, q1, q2 = cirq.LineQubit.range(3)
    yx = cirq.Y(q2) * cirq.X(q0)
    return cirq.unitary(yx)
