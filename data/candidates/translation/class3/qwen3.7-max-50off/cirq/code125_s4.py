# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

class _CircuitGate(cirq.Gate):
    def __init__(self, circuit):
        self._circuit = circuit
        qubits = []
        for op in circuit.all_operations():
            for q in op.qubits:
                if q not in qubits:
                    qubits.append(q)
        self._qubits = qubits
        
    def _num_qubits_(self):
        return len(self._qubits)
        
    def _decompose_(self, qubits):
        qubit_map = dict(zip(self._qubits, qubits))
        return self._circuit.transform_qubits(qubit_map).all_operations()
        
    def _unitary_(self):
        try:
            return cirq.unitary(self._circuit, qubit_order=self._qubits)
        except Exception:
            return NotImplemented

def circ_to_gate(circ):
    return _CircuitGate(circ)
