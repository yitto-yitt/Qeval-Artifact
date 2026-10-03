# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

class CustomGate(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 2
    def _decompose_(self, qubits):
        yield cirq.X(qubits[0])
        yield cirq.H(qubits[1])

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    custom_gate = CustomGate()
    controlled_gate = custom_gate.controlled(num_controls=2)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
