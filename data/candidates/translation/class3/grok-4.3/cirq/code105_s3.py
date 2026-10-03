# EVAL_META: task_id=105, framework=cirq, class=3
import cirq


def initialize_cnot_dihedral():
    circ = cirq.Circuit()
    q = cirq.LineQubit.range(2)
    circ.append(cirq.CX(q[0], q[1]))
    circ.append(cirq.T(q[0]))
    return circ
