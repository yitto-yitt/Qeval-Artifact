# EVAL_META: task_id=41, framework=cirq, class=3
import cirq


def compose_op():
    qubits = cirq.LineQubit.range(3)
    return cirq.X(qubits[0]) * cirq.Y(qubits[2])
