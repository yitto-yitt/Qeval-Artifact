# EVAL_META: task_id=41, framework=cirq, class=3
import cirq
import numpy as np

def compose_op():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(cirq.X(q[0]), cirq.Y(q[2]))
    return cirq.unitary(circuit)
