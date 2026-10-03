# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    if num_qubits == 0:
        return cirq.Circuit()
    return cirq.Circuit(
        cirq.X(q) if i == num_qubits - 1 else cirq.I(q)
        for i, q in enumerate(qubits)
    )
