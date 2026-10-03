# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q = cirq.LineQubit.range(2)
    circ1 = cirq.Circuit(cirq.CNOT(q[0], q[1]), cirq.T(q[0]))
    circ2 = cirq.Circuit(circ1)
    circ2.append(cirq.X(q[1]))
    composed = circ2 + circ1
    return composed
