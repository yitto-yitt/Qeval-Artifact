# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned_parameter(value):
        if value is None:
            return True

        if isinstance(value, str):
            return True

        if isinstance(value, np.ndarray):
            if value.dtype.kind in ("O", "U", "S"):
                return any(_is_unassigned_parameter(item) for item in value.flat)
            return False

        if isinstance(value, (list, tuple, set, frozenset)):
            return any(_is_unassigned_parameter(item) for item in value)

        if isinstance(value, dict):
            return any(
                _is_unassigned_parameter(key) or _is_unassigned_parameter(val)
                for key, val in value.items()
            )

        try:
            free_symbols = getattr(value, "free_symbols", None)
            if free_symbols:
                return True
        except Exception:
            pass

        cls = value.__class__
        module = getattr(cls, "__module__", "") or ""
        name = getattr(cls, "__name__", "") or ""

        if module.startswith("qiskit") and "Parameter" in name:
            try:
                params = getattr(value, "parameters", None)
                if params is not None:
                    return bool(params)
            except Exception:
                pass
            return True

        if module.startswith("pennylane") and name == "Variable":
            return True

        return False

    def _op_has_unassigned_parameters(op):
        params = getattr(op, "data", None)
        if params is None:
            params = getattr(op, "parameters", ())
        return any(_is_unassigned_parameter(param) for param in params)

    def _filtered_tape(tape):
        operations = list(getattr(tape, "operations", ()))
        measurements = list(getattr(tape, "measurements", ()))
        filtered_ops = []

        old_trainable = getattr(tape, "trainable_params", None)
        old_trainable_set = set(old_trainable) if old_trainable is not None else None
        new_trainable = [] if old_trainable_set is not None else None

        old_param_index = 0
        new_param_index = 0

        for op in operations:
            num_params = len(getattr(op, "data", ()))
            keep = not _op_has_unassigned_parameters(op)

            if keep:
                filtered_ops.append(op)
                if old_trainable_set is not None:
                    for local_index in range(num_params):
                        if old_param_index + local_index in old_trainable_set:
                            new_trainable.append(new_param_index + local_index)
                new_param_index += num_params

            old_param_index += num_params

        shots = getattr(tape, "shots", None)
        tape_cls = tape.__class__

        kwargs = {"shots": shots}
        if new_trainable is not None:
            kwargs["trainable_params"] = new_trainable

        try:
            return tape_cls(filtered_ops, measurements, **kwargs)
        except Exception:
            try:
                return qml.tape.QuantumScript(filtered_ops, measurements, **kwargs)
            except TypeError:
                new_tape = qml.tape.QuantumScript(filtered_ops, measurements, shots=shots)
                if new_trainable is not None:
                    new_tape.trainable_params = new_trainable
                return new_tape

    if hasattr(circuit, "operations") and hasattr(circuit, "measurements"):
        return _filtered_tape(circuit)

    if isinstance(circuit, (list, tuple)):
        filtered = [op for op in circuit if not _op_has_unassigned_parameters(op)]
        return tuple(filtered) if isinstance(circuit, tuple) else filtered

    qnode_cls = getattr(qml, "QNode", None)
    if (qnode_cls is not None and isinstance(circuit, qnode_cls)) or callable(circuit):
        @qml.transform
        def _remove_transform(tape):
            new_tape = _filtered_tape(tape)
            return (new_tape,), lambda results: results[0]

        return _remove_transform(circuit)

    if hasattr(circuit, "data") or hasattr(circuit, "parameters"):
        return None if _op_has_unassigned_parameters(circuit) else circuit

    return circuit
