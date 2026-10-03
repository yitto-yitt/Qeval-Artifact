# EVAL_META: task_id=10, framework=cirq, class=3
import cirq


def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.X(q0), cirq.X(q1))
