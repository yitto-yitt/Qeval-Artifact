# EVAL_META: task_id=99, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned(parameter):
        if parameter is None or isinstance(parameter, str):
            return True
        if getattr(parameter, "free_symbols", None):
            return True
        if isinstance(parameter, (list, tuple)):
            return any(is_unassigned(item) for item in parameter)
        if isinstance(parameter, np.ndarray) and parameter.dtype == object:
            return any(is_unassigned(item) for item in parameter.flat)
        return False

    operations = [
        operation
        for operation in circuit.operations
        if not any(is_unassigned(parameter) for parameter in operation.parameters)
    ]
    return circuit.copy(operations=operations)
