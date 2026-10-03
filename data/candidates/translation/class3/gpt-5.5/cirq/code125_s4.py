# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    if isinstance(circ, cirq.FrozenCircuit):
        frozen = circ
    elif hasattr(circ, "freeze"):
        frozen = circ.freeze()
    else:
        frozen = cirq.FrozenCircuit(circ)

    ordered_qubits = tuple(sorted(frozen.all_qubits()))
    qid_shape = tuple(q.dimension for q in ordered_qubits)

    class _CircuitGate(cirq.Gate):
        def __init__(self, circuit, qubits, shape):
            self._circuit = circuit
            self._qubits = tuple(qubits)
            self._qid_shape_value = tuple(shape)

        def num_qubits(self):
            return len(self._qubits)

        def _qid_shape_(self):
            return self._qid_shape_value

        def _decompose_(self, qubits):
            qubit_map = dict(zip(self._qubits, qubits))
            for op in self._circuit.all_operations():
                yield op.with_qubits(*(qubit_map[q] for q in op.qubits))

        def _unitary_(self):
            try:
                return self._circuit.unitary(
                    qubit_order=self._qubits, ignore_terminal_measurements=False
                )
            except (TypeError, ValueError):
                return NotImplemented

        def _has_unitary_(self):
            return self._unitary_() is not NotImplemented

        def _is_parameterized_(self):
            return cirq.is_parameterized(self._circuit)

        def _parameter_names_(self):
            return cirq.parameter_names(self._circuit)

        def _resolve_parameters_(self, resolver, recursive):
            resolved = cirq.resolve_parameters(self._circuit, resolver, recursive)
            if not isinstance(resolved, cirq.FrozenCircuit):
                resolved = resolved.freeze() if hasattr(resolved, "freeze") else cirq.FrozenCircuit(resolved)
            return _CircuitGate(resolved, self._qubits, self._qid_shape_value)

        def __pow__(self, exponent):
            if exponent == 1:
                return self
            if exponent == -1:
                inv = cirq.inverse(self._circuit, default=None)
                if inv is None:
                    return NotImplemented
                if not isinstance(inv, cirq.FrozenCircuit):
                    inv = inv.freeze() if hasattr(inv, "freeze") else cirq.FrozenCircuit(inv)
                return _CircuitGate(inv, self._qubits, self._qid_shape_value)
            return NotImplemented

        def _circuit_diagram_info_(self, args):
            return cirq.CircuitDiagramInfo(
                wire_symbols=tuple("Circuit" for _ in range(len(self._qubits)))
            )

    return _CircuitGate(frozen, ordered_qubits, qid_shape)
