# EVAL_META: task_id=105, framework=cirq, class=3
import cirq


def initialize_cnot_dihedral():
    q = cirq.LineQubit.range(2)
    circ = cirq.Circuit()
    circ.append(cirq.CNOT(q[0], q[1]))
    circ.append(cirq.T(q[0]))
    return circ
