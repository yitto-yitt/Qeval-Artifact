# EVAL_META: task_id=44, framework=cirq, class=3
import cirq
import numpy as np


def tensor_circuits():
    q0, q1, q2 = cirq.LineQubit.range(3)

    top = cirq.Circuit()
    top.append(cirq.X(q0))

    bottom = cirq.Circuit()
    cry = cirq.ry(0.2).controlled()
    bottom.append(cry(q0, q1))

    tensored = cirq.Circuit()
    tensored.append(cirq.X(q0))
    tensored.append(cry(q1, q2))

    return tensored
