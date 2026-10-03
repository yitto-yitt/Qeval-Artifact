# EVAL_META: task_id=66, framework=cirq, class=2
import cirq
from numpy import arccos, sqrt


def w_state():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.ry(2 * arccos(1 / sqrt(3)))(q0),
        cirq.H(q1).controlled_by(q0),
        cirq.CNOT(q1, q2),
        cirq.CNOT(q0, q1),
        cirq.X(q0),
        cirq.measure(q0, q1, q2, key="meas"),
    )
    return circuit
