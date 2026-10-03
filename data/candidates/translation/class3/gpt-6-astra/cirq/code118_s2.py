# EVAL_META: task_id=118, framework=cirq, class=3
import cirq


def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    return cirq.Circuit(
        (cirq.X ** 0.5).on(qubits[3]).controlled_by(*qubits[:3])
    )
