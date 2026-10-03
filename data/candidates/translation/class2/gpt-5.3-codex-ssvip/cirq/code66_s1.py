# EVAL_META: task_id=66, framework=cirq, class=2
import numpy as np
import cirq


def w_state():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    theta = 2 * np.arccos(1 / np.sqrt(3))
    circuit.append(cirq.ry(theta)(q0))
    circuit.append(cirq.H.controlled()(q0, q1))
    circuit.append(cirq.CNOT(q1, q2))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.X(q0))
    circuit.append(cirq.measure(q0, q1, q2, key='m'))
    return circuit
