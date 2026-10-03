# EVAL_META: task_id=66, framework=cirq, class=2
from numpy import arccos, sqrt
import cirq


def w_state():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(2 * arccos(1 / sqrt(3)))(q0))
    circuit.append(cirq.H(q1).controlled_by(q0))
    circuit.append(cirq.X(q2).controlled_by(q1))
    circuit.append(cirq.X(q1).controlled_by(q0))
    circuit.append(cirq.X(q0))
    circuit.append(cirq.measure(q0, q1, q2, key='meas'))
    return circuit
