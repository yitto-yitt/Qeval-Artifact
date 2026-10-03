# EVAL_META: task_id=10, framework=cirq, class=3
import cirq
import numpy as np

def create_operator():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.CNOT(q0, q1),
        cirq.CNOT(q1, q0),
        cirq.CNOT(q0, q1)
    ])
    return circuit
