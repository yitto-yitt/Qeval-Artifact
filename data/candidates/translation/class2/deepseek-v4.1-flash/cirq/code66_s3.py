# EVAL_META: task_id=66, framework=cirq, class=2
import cirq
import numpy as np


def w_state():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.ry(2 * np.arccos(1 / np.sqrt(3))).on(q0),
        cirq.ControlledGate(cirq.H).on(q0, q1),
        cirq.CNOT(q1, q2),
        cirq.CNOT(q0, q1),
        cirq.X(q0),
        cirq.measure(q0, q1, q2, key='result'),
    )
    return circuit
