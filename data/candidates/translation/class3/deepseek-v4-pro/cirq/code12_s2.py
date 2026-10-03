# EVAL_META: task_id=12, framework=cirq, class=3
import cirq


def get_unitary():
    q0, q1 = cirq.LineQubit.range(2)
    circ = cirq.Circuit()
    circ.append(cirq.H(q0))
    circ.append(cirq.CNOT(q0, q1))
    return cirq.unitary(circ, qubit_order=[q1, q0])
