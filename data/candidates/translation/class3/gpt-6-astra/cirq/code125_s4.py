# EVAL_META: task_id=125, framework=cirq, class=3
import cirq


def circ_to_gate(circ):
    frozen = cirq.FrozenCircuit(circ)
    qubits = tuple(cirq.QubitOrder.DEFAULT.order_for(frozen.all_qubits()))

    for op in frozen.all_operations():
        if cirq.is_measurement(op) or (
            not cirq.is_parameterized(op) and not cirq.has_unitary(op)
        ):
            raise ValueError("The circuit must contain only gate-compatible operations.")

    class CircuitGate(cirq.Gate):
        def _qid_shape_(self):
            return tuple(q.dimension for q in qubits)

        def _decompose_(self, target_qubits):
            mapping = dict(zip(qubits, target_qubits))
            return [
                op.transform_qubits(mapping.__getitem__)
                for op in frozen.all_operations()
            ]

        def _is_parameterized_(self):
            return cirq.is_parameterized(frozen)

        def _parameter_names_(self):
            return cirq.parameter_names(frozen)

        def _resolve_parameters_(self, resolver, recursive):
            return circ_to_gate(
                cirq.resolve_parameters(frozen, resolver, recursive=recursive)
            )

        def _has_unitary_(self):
            return cirq.has_unitary(frozen)

        def _unitary_(self):
            if not cirq.has_unitary(frozen):
                return NotImplemented
            return frozen.unitary(qubit_order=qubits)

    return CircuitGate()
