# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import numpy as np
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    def _contains_unassigned(value, seen=None):
        if seen is None:
            seen = set()

        obj_id = id(value)
        if obj_id in seen:
            return False
        seen.add(obj_id)

        if value is None:
            return True

        if isinstance(value, (str, bytes)):
            return True

        if isinstance(value, numbers.Number):
            return False

        module = type(value).__module__.lower()
        if any(name in module for name in ("torch", "tensorflow", "jax", "autograd")):
            return False

        free_symbols = getattr(value, "free_symbols", None)
        if free_symbols:
            return True

        if isinstance(value, dict):
            return any(_contains_unassigned(v, seen) for v in value.values())

        if isinstance(value, (list, tuple, set, frozenset)):
            return any(_contains_unassigned(v, seen) for v in value)

        try:
            arr = np.asarray(value)
            if arr.dtype == object:
                if arr.shape == ():
                    item = arr.item()
                    if item is value:
                        return True
                    return _contains_unassigned(item, seen)
                return any(_contains_unassigned(item, seen) for item in arr.flat)
            if np.issubdtype(arr.dtype, np.number) or np.issubdtype(arr.dtype, np.bool_):
                return False
            if np.issubdtype(arr.dtype, np.str_) or np.issubdtype(arr.dtype, np.bytes_):
                return True
        except Exception:
            pass

        name = type(value).__name__.lower()
        if "symbol" in name or "parameter" in name:
            return True

        return False

    def _has_unassigned_parameter(op):
        params = getattr(op, "parameters", None)
        if params is None:
            params = getattr(op, "data", ())
        return any(_contains_unassigned(param) for param in params)

    def _filtered_script(tape):
        filtered_ops = [op for op in tape.operations if not _has_unassigned_parameter(op)]
        return qml.tape.QuantumScript(
            ops=filtered_ops,
            measurements=list(getattr(tape, "measurements", [])),
            shots=getattr(tape, "shots", None),
        )

    if hasattr(circuit, "operations"):
        return _filtered_script(circuit)

    def _transform(tape):
        return (_filtered_script(tape),), lambda results: results[0]

    return qml.transform(_transform)(circuit)
