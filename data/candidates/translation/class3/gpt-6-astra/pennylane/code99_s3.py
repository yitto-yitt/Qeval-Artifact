# EVAL_META: task_id=99, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned(value):
        if value is None or isinstance(value, str):
            return True
        if bool(getattr(value, "free_symbols", ())):
            return True
        if isinstance(value, np.ndarray):
            return value.dtype == object and any(
                is_unassigned(item) for item in value.flat
            )
        if isinstance(value, (tuple, list)):
            return any(is_unassigned(item) for item in value)
        if isinstance(value, dict):
            return any(is_unassigned(item) for item in value.values())
        return False

    operations = [
        operation
        for operation in circuit.operations
        if not any(is_unassigned(parameter) for parameter in operation.data)
    ]
    return circuit.copy(operations=operations)
