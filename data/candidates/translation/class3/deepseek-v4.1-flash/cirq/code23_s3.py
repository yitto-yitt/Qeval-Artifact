# EVAL_META: task_id=23, framework=cirq, class=3
import cirq

def dj_constant_oracle():
    q = cirq.LineQubit.range(3)
    return cirq.Circuit(cirq.I(q[0]), cirq.I(q[1]), cirq.X(q[2]))
