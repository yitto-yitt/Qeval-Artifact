# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    class CustomGate(cirq.Gate):
        def _num_qubits_(self) -> int:
            return 2
        def _decompose_(self, qubits):
            return [cirq.X(qubits[0]), cirq.H(qubits[1])]
    custom = CustomGate()
    controlled_custom = custom.controlled(2)
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    circuit.append(controlled_custom.on(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
