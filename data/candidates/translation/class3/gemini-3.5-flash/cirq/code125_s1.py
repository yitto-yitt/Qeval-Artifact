# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

class CircuitGate(cirq.Gate):
    def __init__(self, circuit: cirq.Circuit):
        self.circuit = circuit
        self._circuit_qubits = sorted(list(circuit.all_qubits()))

    def _num_qubits_(self) -> int:
        return len(self._circuit_qubits)

    def _decompose_(self, qubits):
        qubit_map = dict(zip(self._circuit_qubits, qubits))
        return [op.with_qubits(*[qubit_map[q] for q in op.qubits]) for op in self.circuit.all_operations()]

    def _has_unitary_(self) -> bool:
        return cirq.has_unitary(self.circuit)

    def _unitary_(self):
        return cirq.unitary(self.circuit)

def circ_to_gate(circ):
    return CircuitGate(circ)
