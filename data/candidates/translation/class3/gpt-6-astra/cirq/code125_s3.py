# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class CircuitGate(cirq.Gate):
        def __init__(self, circuit):
            self._circuit = cirq.FrozenCircuit(circuit)
            self._qubits = tuple(
                cirq.QubitOrder.DEFAULT.order_for(self._circuit.all_qubits())
            )
            for op in self._circuit.all_operations():
                if cirq.is_measurement(op) or (
                    not cirq.is_parameterized(op) and not cirq.has_unitary(op)
                ):
                    raise ValueError("The circuit must contain only unitary operations.")

        def _qid_shape_(self):
            return tuple(q.dimension for q in self._qubits)

        def _decompose_(self, qubits):
            mapping = dict(zip(self._qubits, qubits))
            return [
                op.transform_qubits(mapping)
                for op in self._circuit.all_operations()
            ]

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return CircuitGate(
                cirq.resolve_parameters(self._circuit, resolver, recursive)
            )

    return CircuitGate(circ)
