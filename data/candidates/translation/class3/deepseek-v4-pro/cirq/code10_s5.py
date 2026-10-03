# EVAL_META: task_id=10, framework=cirq, class=3
import cirq

def create_operator():
    q = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.X(q[0]), cirq.X(q[1]))
