# EVAL_META: task_id=58, framework=cirq, class=3
import cirq
from numpy import pi

def create_ch_gate():
    control, target = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.ry(pi / 4)(target),
        cirq.CNOT(control, target),
        cirq.ry(-pi / 4)(target),
    )
