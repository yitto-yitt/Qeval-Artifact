# EVAL_META: task_id=58, framework=cirq, class=3
import cirq
import numpy as np

def create_ch_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.ry(np.pi / 4).on(q1),
        cirq.CNOT(q0, q1),
        cirq.ry(-np.pi / 4).on(q1),
    )
    return circuit
