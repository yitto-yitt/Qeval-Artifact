# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned(value):
        if value is None or isinstance(value, str):
            return True
        if getattr(value, "free_symbols", None):
            return True
        if isinstance(value, (list, tuple)):
            return any(is_unassigned(item) for item in value)
        if isinstance(value, np.ndarray) and value.dtype == object:
            return any(is_unassigned(item) for item in value.flat)
        return False

    operations = [
        operation
        for operation in circuit.operations
        if not any(is_unassigned(parameter) for parameter in operation.data)
    ]

    return qml.tape.QuantumScript(
        ops=operations,
        measurements=list(circuit.measurements),
        shots=circuit.shots,
    )
