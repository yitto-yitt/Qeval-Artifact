# EVAL_META: task_id=109, framework=cirq, class=3
import cirq

def circuit():
    q = cirq.LineQubit(0)
    theta = cirq.Symbol("th")
    return cirq.Circuit(
        cirq.H(q),
        cirq.rz(theta).on(q),
    )
