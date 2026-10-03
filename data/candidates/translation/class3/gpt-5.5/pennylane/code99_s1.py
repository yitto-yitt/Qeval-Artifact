# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import numpy as np
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned_parameter(param):
        if param is None:
            return True

        if isinstance(param, str):
            return True

        if isinstance(param, numbers.Number):
            return False

        if isinstance(param, dict):
            return any(is_unassigned_parameter(v) for v in param.values())

        if isinstance(param, (list, tuple, set)):
            return any(is_unassigned_parameter(v) for v in param)

        free_symbols = getattr(param, "free_symbols", None)
        if free_symbols:
            return True

        if getattr(param, "is_Symbol", False):
            return True

        if type(param).__name__ in {"Parameter", "ParameterExpression", "Variable"}:
            return True

        try:
            arr = np.asarray(param)
            if arr.dtype == object:
                return any(is_unassigned_parameter(x) for x in arr.flat)
            return False
        except Exception:
            return False

    operations = list(getattr(circuit, "operations", []))
    measurements = list(getattr(circuit, "measurements", []))

    filtered_operations = []
    for op in operations:
        params = getattr(op, "data", getattr(op, "parameters", ()))
        if not params or not any(is_unassigned_parameter(param) for param in params):
            filtered_operations.append(op)

    return qml.tape.QuantumScript(
        filtered_operations,
        measurements,
        shots=getattr(circuit, "shots", None),
    )
