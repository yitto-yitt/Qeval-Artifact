# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class _CircuitGate(cirq.Gate):
        def __init__(self, circuit, qubits=None):
            if isinstance(circuit, cirq.FrozenCircuit):
                self._circuit = circuit
            elif hasattr(circuit, "freeze"):
                self._circuit = circuit.freeze()
            else:
                self._circuit = cirq.FrozenCircuit(circuit)

            if qubits is None:
                self._qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(self._circuit.all_qubits()))
            else:
                self._qubits = tuple(qubits)

        def _num_qubits_(self):
            return len(self._qubits)

        def _qid_shape_(self):
            return tuple(getattr(q, "dimension", 2) for q in self._qubits)

        def _decompose_(self, qubits):
            qubit_map = dict(zip(self._qubits, qubits))
            for moment in self._circuit:
                for op in moment.operations:
                    yield op.transform_qubits(lambda q: qubit_map[q])

        def _has_unitary_(self):
            return cirq.has_unitary(self._circuit)

        def _unitary_(self):
            if cirq.is_parameterized(self._circuit):
                return NotImplemented
            try:
                return cirq.unitary(self._circuit, qubit_order=self._qubits, default=NotImplemented)
            except (TypeError, ValueError):
                return NotImplemented

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return _CircuitGate(cirq.resolve_parameters(self._circuit, resolver, recursive), self._qubits)

        def _circuit_diagram_info_(self, args):
            return tuple("Circuit" for _ in self._qubits)

        def __repr__(self):
            return f"_CircuitGate({self._circuit!r})"

    return _CircuitGate(circ)
