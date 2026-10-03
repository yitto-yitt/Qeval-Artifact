# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

class _CustomGate(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 2

    def _decompose_(self, qubits):
        yield cirq.X(qubits[0])
        yield cirq.H(qubits[1])

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    custom_gate = _CustomGate()
    controlled_gate = cirq.ControlledGate(custom_gate, num_controls=2)
    
    circuit = cirq.Circuit(
        controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2])
    )
    
    return circuit
