# EVAL_META: task_id=41, framework=cirq, class=3
import cirq

def compose_op():
    qubits = cirq.LineQubit.range(3)
    yx = cirq.Y(qubits[2]) * cirq.X(qubits[0])
    return yx
