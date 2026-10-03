# EVAL_META: task_id=90, framework=cirq, class=3
import cirq


def create_custom_controlled():
    q = cirq.LineQubit.range(4)
    custom_gate = cirq.CircuitOperation(
        cirq.FrozenCircuit(
            cirq.X(cirq.LineQubit(0)),
            cirq.H(cirq.LineQubit(1)),
        )
    ).with_controls(cirq.LineQubit(2), cirq.LineQubit(3))
    mapped_op = custom_gate.with_qubit_mapping({
        cirq.LineQubit(2): q[0],
        cirq.LineQubit(3): q[3],
        cirq.LineQubit(0): q[1],
        cirq.LineQubit(1): q[2],
    })
    return cirq.Circuit(mapped_op)
