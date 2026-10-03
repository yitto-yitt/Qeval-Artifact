# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    q0, q1, q2 = cirq.LineQubit.range(3)
    cry_gate = cirq.ry(0.2).controlled()
    circuit = cirq.Circuit([
        cry_gate.on(q0, q1),
        cirq.X(q2)
    ])
    return circuit
