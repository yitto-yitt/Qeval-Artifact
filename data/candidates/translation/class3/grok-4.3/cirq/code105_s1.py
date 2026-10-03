# EVAL_META: task_id=105, framework=cirq, class=3
import cirq

def initialize_cnot_dihedral():
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    circ = cirq.Circuit(cirq.CNOT(q0, q1), cirq.T(q0))
    return circ
