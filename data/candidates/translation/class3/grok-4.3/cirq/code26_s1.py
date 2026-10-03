# EVAL_META: task_id=26, framework=cirq, class=3
import cirq

def bell_dag():
    q = cirq.LineQubit.range(3)
    circ = cirq.Circuit()
    circ.append(cirq.H(q[0]))
    circ.append(cirq.CNOT(q[0], q[1]))
    circ.append(cirq.measure(q[0], key="c_0"))
    return circ
