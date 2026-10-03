# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if hasattr(circ, "to_operation"):
        try:
            return circ.to_operation()
        except Exception:
            pass

    if isinstance(circ, qml.operation.Operator):
        return circ

    tape_like = circ

    if not hasattr(tape_like, "operations"):
        for attr in ("tape", "qtape", "_tape"):
            candidate = getattr(circ, attr, None)
            if candidate is not None and hasattr(candidate, "operations"):
                tape_like = candidate
                break

    if not hasattr(tape_like, "operations") and hasattr(circ, "construct"):
        try:
            candidate = circ.construct((), {})
            if candidate is None:
                candidate = getattr(circ, "tape", None) or getattr(circ, "qtape", None) or getattr(circ, "_tape", None)
            if candidate is not None and hasattr(candidate, "operations"):
                tape_like = candidate
        except Exception:
            pass

    if not hasattr(tape_like, "operations") and callable(circ):
        try:
            tape_like = qml.tape.make_qscript(circ)()
        except Exception:
            pass

    if hasattr(tape_like, "operations"):
        operations = list(tape_like.operations)
        wires = getattr(tape_like, "wires", None)
    elif isinstance(circ, (list, tuple)):
        operations = list(circ)
        wires = None
    else:
        raise TypeError("circ must be a PennyLane circuit, tape, operator, callable, or sequence of operators")

    if wires is None:
        wire_labels = []
        for op in operations:
            for wire in op.wires:
                if wire not in wire_labels:
                    wire_labels.append(wire)
        wires = qml.wires.Wires(wire_labels)
    else:
        wires = qml.wires.Wires(wires)

    class _CircuitGate(qml.operation.Operation):
        num_wires = qml.operation.AnyWires
        num_params = 0
        grad_method = None

        def __init__(self, operations, wires=None, base_wires=None, id=None):
            if base_wires is None:
                base_wires = wires
            self._hyperparameters = {
                "operations": tuple(operations),
                "base_wires": qml.wires.Wires(base_wires),
            }
            super().__init__(wires=wires, id=id)

        @staticmethod
        def compute_decomposition(wires=None, operations=None, base_wires=None):
            wires = qml.wires.Wires(wires)
            base_wires = qml.wires.Wires(base_wires)
            operations = tuple(operations or ())

            if not operations:
                return [qml.Identity(wires=wires)] if len(wires) else []

            wire_map = dict(zip(base_wires, wires))
            return [op.map_wires(wire_map) for op in operations]

        def decomposition(self):
            return self.compute_decomposition(wires=self.wires, **self.hyperparameters)

    return _CircuitGate(operations, wires=wires, base_wires=wires)
