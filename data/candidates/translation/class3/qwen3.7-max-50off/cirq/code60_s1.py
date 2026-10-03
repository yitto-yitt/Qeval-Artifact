# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        (cirq.S**-1)(q1),
        cirq.CX(q0, q1),
        cirq.S(q1)
    )
