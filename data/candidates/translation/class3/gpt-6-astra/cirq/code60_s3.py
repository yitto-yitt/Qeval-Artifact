# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    control, target = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.S(target) ** -1,
        cirq.CNOT(control, target),
        cirq.S(target),
    )
