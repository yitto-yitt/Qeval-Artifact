# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

class CircuitGate(cirq.Gate):
    def __init__(self, circuit: cirq.Circuit):
        self.circuit = circuit
        self.qubits = sorted(circuit.all_qubits())

    def _num_qubits_(self) -> int:
        return len(self.qubits)

    def _decompose_(self, qubits):
        qubit_map = dict(zip(self.qubits, qubits))
        return self.circuit.transform_qubits(lambda q: qubit_map[q]).all_operations()

    def _unitary_(self):
        return cirq.unitary(self.circuit)


def circ_to_gate(circ: cirq.Circuit) -> cirq.Gate:
    return CircuitGate(circ)
