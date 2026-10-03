# EVAL_META: task_id=67, framework=cirq, class=1
from numpy import pi
import cirq


def chsh_circuit(alice, bob):
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.ry(0 if alice == 0 else -pi / 2)(q0),
        cirq.measure(q0, key="c0"),
        cirq.ry(-pi / 4 if bob == 0 else pi / 4)(q1),
        cirq.measure(q1, key="c1"),
        strategy=cirq.InsertStrategy.NEW,
    )
