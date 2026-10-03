# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q0, q1, q2 = cirq.LineQubit.range(3)
    return cirq.Circuit(
        cirq.ControlledGate(cirq.ry(0.2)).on(q0, q1),
        cirq.X(q2),
    )
