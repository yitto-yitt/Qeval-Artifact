# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)

    circ1 = cirq.Circuit(
        cirq.Moment([cirq.CNOT(q0, q1)]),
        cirq.Moment([cirq.T(q0)]),
    )

    circ2 = cirq.Circuit(
        cirq.Moment([cirq.CNOT(q0, q1)]),
        cirq.Moment([cirq.T(q0)]),
        cirq.Moment([cirq.X(q1)]),
    )

    return circ2 + circ1
