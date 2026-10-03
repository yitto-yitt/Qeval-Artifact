# EVAL_META: task_id=90, framework=cirq, class=3
import cirq


def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    x_gate = cirq.X.controlled(num_controls=2)
    h_gate = cirq.H.controlled(num_controls=2)
    circuit.append(x_gate.on(qubits[0], qubits[3], qubits[1]))
    circuit.append(h_gate.on(qubits[0], qubits[3], qubits[2]))
    return circuit
