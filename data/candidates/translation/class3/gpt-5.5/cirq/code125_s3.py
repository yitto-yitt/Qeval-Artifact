# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class _CircuitGate(cirq.Gate):
        def __init__(self, circuit):
            self._circuit = circuit if isinstance(circuit, cirq.FrozenCircuit) else circuit.freeze()
            self._qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(self._circuit.all_qubits()))
            self._qid_shape_value = tuple(q.dimension for q in self._qubits)

        def _num_qubits_(self):
            return len(self._qubits)

        def _qid_shape_(self):
            return self._qid_shape_value

        def _decompose_(self, qubits):
            qubit_map = dict(zip(self._qubits, qubits))
            for moment in self._circuit:
                for op in moment.operations:
                    yield op.transform_qubits(lambda q: qubit_map[q])

        def _unitary_(self):
            try:
                return self._circuit.unitary(qubit_order=self._qubits)
            except (TypeError, ValueError):
                return NotImplemented

        def _has_unitary_(self):
            return cirq.has_unitary(self._circuit)

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return _CircuitGate(cirq.resolve_parameters(self._circuit, resolver, recursive))

        def _circuit_diagram_info_(self, args):
            return ["Circuit"] * len(self._qubits)

        def __repr__(self):
            return f"_CircuitGate({self._circuit!r})"

    return _CircuitGate(circ)
