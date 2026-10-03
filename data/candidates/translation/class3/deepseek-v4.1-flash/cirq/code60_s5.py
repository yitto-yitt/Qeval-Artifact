# EVAL_META: task_id=60, framework=cirq, class=3
import cirq


def create_cy_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        (cirq.S**-1).on(q1),
        cirq.CNOT(q0, q1),
        cirq.S.on(q1),
    )
    return circuit
