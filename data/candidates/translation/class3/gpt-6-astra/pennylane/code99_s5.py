# EVAL_META: task_id=99, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned(parameter):
        free_symbols = getattr(parameter, "free_symbols", None)
        if free_symbols is not None and bool(free_symbols):
            return True
        if isinstance(parameter, (list, tuple)):
            return any(is_unassigned(value) for value in parameter)
        if isinstance(parameter, np.ndarray) and parameter.dtype == object:
            return any(is_unassigned(value) for value in parameter.flat)
        return False

    operations = [
        operation
        for operation in circuit.operations
        if not any(is_unassigned(parameter) for parameter in operation.data)
    ]
    return circuit.copy(operations=operations)
