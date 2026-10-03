# EVAL_META: task_id=5, framework=cirq, class=2
import cirq


def create_state_prep():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[1]))
    return circuit
