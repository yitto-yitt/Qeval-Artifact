# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import numpy as np
import pennylane as qml


def _is_assigned(param):
    """Return True if the parameter is a concrete numeric value."""
    if isinstance(param, numbers.Number):
        return True
    try:
        np.asarray(param, dtype=float)
        return True
    except (TypeError, ValueError):
        return False


def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        params = op.parameters
        if all(_is_assigned(p) for p in params):
            new_ops.append(op)

    new_tape = qml.tape.QuantumTape(
        ops=new_ops,
        measurements=list(circuit.measurements),
    )
    return new_tape
