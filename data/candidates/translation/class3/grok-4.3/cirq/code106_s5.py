# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)
    circ1 = cirq.Circuit(cirq.CNOT(q0, q1), cirq.T(q0))
    circ2 = circ1.copy()
    circ2.append(cirq.X(q1))
    composed = circ2 + circ1
    return composed
