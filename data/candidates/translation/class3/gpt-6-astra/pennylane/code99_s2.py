# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from sympy import Symbol

def remove_unassigned_parameterized_gates(circuit):
    operations = [
        operation
        for operation in circuit.operations
        if not (
            operation.parameters
            and isinstance(operation.parameters[0], Symbol)
        )
    ]
    return circuit.copy(operations=operations)
