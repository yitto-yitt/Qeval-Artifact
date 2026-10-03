# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq

def compose_op():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(cirq.Y(q0), cirq.X(q2))
    return cirq.unitary(circuit)
