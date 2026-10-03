# EVAL_META: task_id=41, framework=cirq, class=3
import cirq

def compose_op():
    q = cirq.LineQubit.range(3)
    yx = cirq.X.on(q[0]) * cirq.Y.on(q[2])
    return yx
