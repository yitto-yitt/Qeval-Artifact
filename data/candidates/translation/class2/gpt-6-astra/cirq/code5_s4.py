# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    q1, q0 = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.I(q1), cirq.X(q0))
