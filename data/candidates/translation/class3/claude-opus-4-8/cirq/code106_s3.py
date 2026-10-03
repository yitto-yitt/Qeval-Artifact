# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    q = cirq.LineQubit.range(2)

    circ1 = cirq.Circuit()
    circ1.append(cirq.CNOT(q[0], q[1]))
    circ1.append(cirq.T(q[0]))

    circ2 = circ1.copy()
    circ2.append(cirq.X(q[1]))

    composed = cirq.Circuit()
    composed.append(circ1.all_operations())
    composed.append(circ2.all_operations())

    return composed
