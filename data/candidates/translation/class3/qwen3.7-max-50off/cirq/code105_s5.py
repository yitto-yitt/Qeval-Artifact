# EVAL_META: task_id=105, framework=cirq, class=3
import cirq

def initialize_cnot_dihedral():
    q0, q1 = cirq.LineQubit.range(2)
    circ = cirq.Circuit()
    circ.append(cirq.CNOT(q0, q1))
    circ.append(cirq.T(q0))
    return circ
