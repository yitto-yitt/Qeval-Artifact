# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(
        cirq.X(qubit) if index == num_qubits - 1 else cirq.I(qubit)
        for index, qubit in enumerate(qubits)
    )
