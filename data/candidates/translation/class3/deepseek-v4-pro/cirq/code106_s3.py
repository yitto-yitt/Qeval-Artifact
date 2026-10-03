# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)

    circ1 = cirq.Circuit(cirq.CNOT(q0, q1), cirq.T(q0))
    circ2 = circ1 + cirq.Circuit(cirq.X(q1))

    composed_elem = circ1 + circ2
    return composed_elem
