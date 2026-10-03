# EVAL_META: task_id=59, framework=cirq, class=3
import cirq

def create_cz_gate():
    control, target = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.H(target),
        cirq.CNOT(control, target),
        cirq.H(target),
    )
