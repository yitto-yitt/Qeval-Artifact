# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import numpy as np
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    def has_unassigned_parameter(value):
        if value is None:
            return True

        if isinstance(value, numbers.Number):
            return False

        free_symbols = getattr(value, "free_symbols", None)
        if free_symbols is not None:
            try:
                if len(free_symbols) > 0:
                    return True
                complex(value)
                return False
            except Exception:
                return True

        if isinstance(value, (str, bytes)):
            return True

        if isinstance(value, dict):
            return any(has_unassigned_parameter(v) for v in value.values())

        if isinstance(value, (list, tuple, set)):
            return any(has_unassigned_parameter(v) for v in value)

        try:
            arr = qml.math.asarray(value)
            dtype = getattr(arr, "dtype", None)
            dtype_str = str(dtype) if dtype is not None else ""

            if dtype_str == "object" or dtype_str.startswith("<U") or dtype_str.startswith("|S"):
                try:
                    obj_arr = np.asarray(value, dtype=object)
                    return any(has_unassigned_parameter(v) for v in obj_arr.flat)
                except Exception:
                    return True

            return False
        except Exception:
            name = type(value).__name__.lower()
            module = type(value).__module__.lower()
            if (
                "parameter" in name
                or "variable" in name
                or "symbol" in name
                or "sympy" in module
            ):
                return True
            return True

    def operation_has_unassigned_parameters(op):
        params = getattr(op, "parameters", getattr(op, "data", ()))
        return any(has_unassigned_parameter(param) for param in params)

    if hasattr(circuit, "operations"):
        kept_operations = [
            op for op in circuit.operations if not operation_has_unassigned_parameters(op)
        ]
        measurements = list(getattr(circuit, "measurements", []))
        shots = getattr(circuit, "shots", None)

        try:
            return circuit.__class__(kept_operations, measurements, shots=shots)
        except Exception:
            return qml.tape.QuantumScript(kept_operations, measurements, shots=shots)

    if isinstance(circuit, tuple):
        return tuple(op for op in circuit if not operation_has_unassigned_parameters(op))

    if isinstance(circuit, list):
        return [op for op in circuit if not operation_has_unassigned_parameters(op)]

    return circuit
