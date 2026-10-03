# EVAL_META: task_id=67, framework=cirq, class=1
from numpy import pi
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    ops = [cirq.H(q0), cirq.CNOT(q0, q1)]
    if alice == 0:
        ops.append(cirq.Ry(0)(q0))
    else:
        ops.append(cirq.Ry(-pi / 2)(q0))
    ops.append(cirq.measure(q0, key="0"))
    if bob == 0:
        ops.append(cirq.Ry(-pi / 4)(q1))
    else:
        ops.append(cirq.Ry(pi / 4)(q1))
    ops.append(cirq.measure(q1, key="1"))
    return cirq.Circuit(ops)
