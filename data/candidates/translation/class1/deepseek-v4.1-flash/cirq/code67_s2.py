# EVAL_META: task_id=67, framework=cirq, class=1
from numpy import pi
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    moments = []
    moments.append(cirq.Moment([cirq.H(q0)]))
    moments.append(cirq.Moment([cirq.CNOT(q0, q1)]))
    if alice == 0:
        moments.append(cirq.Moment([cirq.ry(0).on(q0)]))
    else:
        moments.append(cirq.Moment([cirq.ry(-pi / 2).on(q0)]))
    moments.append(cirq.Moment([cirq.measure(q0, key='m0')]))
    if bob == 0:
        moments.append(cirq.Moment([cirq.ry(-pi / 4).on(q1)]))
    else:
        moments.append(cirq.Moment([cirq.ry(pi / 4).on(q1)]))
    moments.append(cirq.Moment([cirq.measure(q1, key='m1')]))
    return cirq.Circuit(moments)
