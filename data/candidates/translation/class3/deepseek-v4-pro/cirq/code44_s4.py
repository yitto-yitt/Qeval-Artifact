# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q = cirq.LineQubit.range(3)
    cry = cirq.ry(0.2).controlled(1)
    return cirq.Circuit(
        cry.on(q[0], q[1]),
        cirq.X.on(q[2]),
    )
