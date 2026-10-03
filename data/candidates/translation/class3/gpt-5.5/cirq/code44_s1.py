# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.ry(0.2).on(q1).controlled_by(q0),
        cirq.X(q2),
    )
    return circuit
