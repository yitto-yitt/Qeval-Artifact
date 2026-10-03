# EVAL_META: task_id=44, framework=cirq, class=3
import cirq
import numpy as np


def tensor_circuits():
    q = cirq.LineQubit.range(3)

    top = cirq.Circuit()
    top.append(cirq.X(q[0]))

    bottom = cirq.Circuit()
    bottom.append(cirq.ry(0.2).on(q[2]).controlled_by(q[1]))

    tensored = cirq.Circuit()
    tensored.append(top.all_operations())
    tensored.append(bottom.all_operations())

    return tensored
