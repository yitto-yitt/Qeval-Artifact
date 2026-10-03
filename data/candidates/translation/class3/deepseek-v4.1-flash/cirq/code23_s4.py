# EVAL_META: task_id=23, framework=cirq, class=3
import cirq

def dj_constant_oracle():
    q0, q1, q2 = cirq.LineQubit.range(3)
    return cirq.Circuit(cirq.X(q2))
