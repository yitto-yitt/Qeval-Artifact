# EVAL_META: task_id=67, framework=cirq, class=1
from numpy import pi
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    c = cirq.Circuit()

    c.append(cirq.H(q0))
    c.append(cirq.CNOT(q0, q1))
    c.append(cirq.Moment())

    if alice == 0:
        c.append(cirq.ry(0).on(q0))
    else:
        c.append(cirq.ry(-pi / 2).on(q0))
    c.append(cirq.measure(q0, key="c0"))

    if bob == 0:
        c.append(cirq.ry(-pi / 4).on(q1))
    else:
        c.append(cirq.ry(pi / 4).on(q1))
    c.append(cirq.measure(q1, key="c1"))

    return c
