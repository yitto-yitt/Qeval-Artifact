# EVAL_META: task_id=66, framework=cirq, class=2
from numpy import arccos, sqrt
import cirq


def w_state():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(2 * arccos(1 / sqrt(3)))(q[0]))
    circuit.append(cirq.H(q[1]).controlled_by(q[0]))
    circuit.append(cirq.CNOT(q[1], q[2]))
    circuit.append(cirq.CNOT(q[0], q[1]))
    circuit.append(cirq.X(q[0]))
    circuit.append(cirq.measure(q[0], q[1], q[2], key='m'))
    return circuit
