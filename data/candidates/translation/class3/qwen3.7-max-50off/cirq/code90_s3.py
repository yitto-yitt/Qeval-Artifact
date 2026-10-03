# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

class XHGate(cirq.Gate):
    def _num_qubits_(self):
        return 2
    
    def _decompose_(self, qubits):
        yield cirq.X(qubits[0])
        yield cirq.H(qubits[1])

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    custom_gate = XHGate()
    controlled_gate = cirq.ControlledGate(custom_gate, num_controls=2)
    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
