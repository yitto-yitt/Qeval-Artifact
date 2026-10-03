# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    """Return a Cirq circuit preparing the state |1⟩ on `num_qubits` qubits."""
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit(cirq.X(qubits[0]))
    return circuit
