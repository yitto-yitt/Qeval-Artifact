# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit(cirq.I(q) for q in qubits)
    if qubits:
        circuit.append(cirq.X(qubits[-1]))
    return circuit
