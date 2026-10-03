# EVAL_META: task_id=57, framework=cirq, class=3
import cirq

def create_swap_gate():
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.CNOT(q0, q1),
        cirq.CNOT(q1, q0),
        cirq.CNOT(q0, q1),
    )
