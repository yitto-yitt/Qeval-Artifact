# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class _CircuitAsGate(cirq.Gate):
        def __init__(self, circuit, qubits=None):
            self._circuit = cirq.FrozenCircuit(circuit)
            self._qubits = tuple(
                cirq.QubitOrder.DEFAULT.order_for(self._circuit.all_qubits())
                if qubits is None
                else qubits
            )

        def _num_qubits_(self):
            return len(self._qubits)

        def _qid_shape_(self):
            return tuple(q.dimension for q in self._qubits)

        def _decompose_(self, qubits):
            qubit_map = dict(zip(self._qubits, qubits))
            for moment in self._circuit:
                yield [op.transform_qubits(lambda q: qubit_map[q]) for op in moment.operations]

        def _unitary_(self):
            if cirq.is_parameterized(self._circuit):
                return NotImplemented
            try:
                return self._circuit.unitary(qubit_order=self._qubits)
            except (TypeError, ValueError):
                return NotImplemented

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return _CircuitAsGate(
                cirq.resolve_parameters(self._circuit, resolver, recursive),
                self._qubits,
            )

        def _circuit_diagram_info_(self, args):
            return tuple(f"CircuitGate[{i}]" for i in range(len(self._qubits)))

        def __repr__(self):
            return f"circ_to_gate({self._circuit!r})"

    return _CircuitAsGate(circ)
