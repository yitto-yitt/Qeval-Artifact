# EVAL_META: task_id=27, framework=cirq, class=3
import cirq

def apply_op_back():
    q = cirq.LineQubit.range(3)
    circ = cirq.Circuit()
    circ.append(cirq.H(q[0]))
    circ.append(cirq.CX(q[0], q[1]))
    circ.append(cirq.H(q[0]))
    return circ
