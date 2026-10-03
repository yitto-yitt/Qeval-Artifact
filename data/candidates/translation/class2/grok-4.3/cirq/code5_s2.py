# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.X(qubits[0]))
    return circuit
