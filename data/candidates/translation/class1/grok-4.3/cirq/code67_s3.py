# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
from numpy import pi


def chsh_circuit(alice, bob):
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    qc = cirq.Circuit()
    qc.append(cirq.H(q0))
    qc.append(cirq.CNOT(q0, q1))
    if alice == 0:
        qc.append(cirq.Ry(0)(q0))
    else:
        qc.append(cirq.Ry(-pi / 2)(q0))
    qc.append(cirq.measure(q0, key="0"))
    if bob == 0:
        qc.append(cirq.Ry(-pi / 4)(q1))
    else:
        qc.append(cirq.Ry(pi / 4)(q1))
    qc.append(cirq.measure(q1, key="1"))
    return qc
