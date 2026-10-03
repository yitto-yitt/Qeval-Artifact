# EVAL_META: task_id=67, framework=cirq, class=1
from numpy import pi
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    qc = cirq.Circuit()
    qc.append(cirq.H(q0))
    qc.append(cirq.CNOT(q0, q1))
    if alice == 0:
        qc.append(cirq.ry(0).on(q0))
    else:
        qc.append(cirq.ry(-pi / 2).on(q0))
    qc.append(cirq.measure(q0, key='0'))
    if bob == 0:
        qc.append(cirq.ry(-pi / 4).on(q1))
    else:
        qc.append(cirq.ry(pi / 4).on(q1))
    qc.append(cirq.measure(q1, key='1'))
    return qc
