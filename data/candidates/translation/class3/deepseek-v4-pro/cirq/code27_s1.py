# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    q = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit([
        cirq.H(q[0]),
        cirq.CX(q[0], q[1]),
        cirq.H(q[0]),
    ])
    return circuit
