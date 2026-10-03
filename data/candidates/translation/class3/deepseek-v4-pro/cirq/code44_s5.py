# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q = cirq.LineQubit.range(3)
    cry = cirq.ry(0.2)(q[1]).controlled_by(q[0])
    x = cirq.X(q[2])
    return cirq.Circuit(cry, x)
