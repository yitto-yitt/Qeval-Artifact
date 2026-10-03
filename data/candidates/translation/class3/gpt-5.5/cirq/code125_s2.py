# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    class _CircuitAsGate(cirq.Gate):
        def __init__(self, circuit):
            self._circuit = circuit.freeze() if hasattr(circuit, "freeze") else cirq.FrozenCircuit(circuit)
            self._qubits = tuple(sorted(self._circuit.all_qubits()))
            self._qid_shape_value = tuple(getattr(q, "dimension", 2) for q in self._qubits)
            self._name = getattr(circuit, "name", None) or "Circuit"

        def _qid_shape_(self):
            return self._qid_shape_value

        def _num_qubits_(self):
            return len(self._qubits)

        def _decompose_(self, qubits):
            qubit_map = dict(zip(self._qubits, qubits))
            for op in self._circuit.all_operations():
                yield op.transform_qubits(lambda q: qubit_map[q])

        def _unitary_(self):
            return cirq.unitary(self._circuit, qubit_order=self._qubits, default=NotImplemented)

        def _has_unitary_(self):
            return cirq.has_unitary(self._circuit)

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            return _CircuitAsGate(cirq.resolve_parameters(self._circuit, resolver, recursive))

        def _circuit_diagram_info_(self, args):
            return cirq.CircuitDiagramInfo(wire_symbols=(self._name,) * len(self._qubits))

        def __repr__(self):
            return f"_CircuitAsGate({self._circuit!r})"

        def __eq__(self, other):
            return (
                hasattr(other, "_circuit")
                and hasattr(other, "_qubits")
                and self._circuit == other._circuit
                and self._qubits == other._qubits
            )

        def __hash__(self):
            return hash((self._circuit, self._qubits))

    return _CircuitAsGate(circ)
