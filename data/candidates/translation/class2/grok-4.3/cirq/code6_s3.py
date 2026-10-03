# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    if num_qubits == 0:
        return cirq.Circuit()
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(cirq.X(qubits[-1]))
