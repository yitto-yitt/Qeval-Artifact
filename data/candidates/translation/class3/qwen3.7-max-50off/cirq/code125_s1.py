# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

class _CircuitGate(cirq.Gate):
    def __init__(self, circuit):
        self._circuit = circuit
        self._qubits = sorted(circuit.all_qubits())
        
    def _num_qubits_(self):
        return len(self._qubits)
        
    def _unitary_(self):
        try:
            return cirq.unitary(self._circuit)
        except Exception:
            return NotImplemented
            
    def _decompose_(self, qubits):
        qubit_map = dict(zip(self._qubits, qubits))
        return self._circuit.transform_qubits(qubit_map).all_operations()

def circ_to_gate(circ):
    return _CircuitGate(circ)
