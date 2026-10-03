# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    qubits = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.I(qubits[0]), cirq.X(qubits[1]))
