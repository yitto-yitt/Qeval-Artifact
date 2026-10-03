# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class CircuitGate(cirq.Gate):
        def __init__(self, circuit):
            self._circuit = cirq.FrozenCircuit(circuit)
            self._qubits = tuple(
                cirq.QubitOrder.DEFAULT.order_for(self._circuit.all_qubits())
            )

        def _num_qubits_(self):
            return len(self._qubits)

        def _qid_shape_(self):
            return tuple(q.dimension for q in self._qubits)

        def _decompose_(self, qubits):
            mapping = dict(zip(self._qubits, qubits))
            return self._circuit.transform_qubits(mapping).all_operations()

        def _unitary_(self):
            return cirq.unitary(self._circuit, default=NotImplemented)

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return CircuitGate(
                cirq.resolve_parameters(self._circuit, resolver, recursive)
            )

    return CircuitGate(circ)
