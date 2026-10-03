# EVAL_META: task_id=59, framework=cirq, class=3
import cirq

def create_cz_gate():
    q = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.H(q[1]),
        cirq.CNOT(q[0], q[1]),
        cirq.H(q[1])
    )
