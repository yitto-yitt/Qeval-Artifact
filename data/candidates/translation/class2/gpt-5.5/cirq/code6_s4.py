# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    if num_qubits < 1:
        raise ValueError("num_qubits must be at least 1")
    circuit = cirq.Circuit(cirq.I(q) for q in qubits)
    circuit.append(cirq.X(qubits[-1]))
    return circuit
