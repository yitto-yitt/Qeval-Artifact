# EVAL_META: task_id=44, framework=cirq, class=3
import cirq


def tensor_circuits():
    top_q = cirq.LineQubit(0)
    top = cirq.Circuit(cirq.X(top_q))

    bottom_q0, bottom_q1 = cirq.LineQubit.range(1, 3)
    bottom = cirq.Circuit(cirq.ry(0.2).on(bottom_q1).controlled_by(bottom_q0))

    tensored = bottom + top
    return tensored
