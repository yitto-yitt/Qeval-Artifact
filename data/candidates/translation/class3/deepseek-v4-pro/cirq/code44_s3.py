# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.ry(0.2).on(q[1]).controlled_by(q[0]),
        cirq.X.on(q[2]),
    )
    return circuit
