# EVAL_META: task_id=99, framework=pennylane, class=3
import numbers
import pennylane as qml
import numpy as np


def _is_assigned(value):
    if isinstance(value, numbers.Number):
        return True
    try:
        np.asarray(value, dtype=float)
        return True
    except (TypeError, ValueError):
        return False


def remove_unassigned_parameterized_gates(circuit):
    if hasattr(circuit, "operations"):
        ops = list(circuit.operations)
        measurements = list(circuit.measurements)
    else:
        ops = list(circuit)
        measurements = []

    kept_ops = []
    for op in ops:
        params = list(getattr(op, "parameters", []))
        if len(params) == 0:
            kept_ops.append(op)
            continue
        if all(_is_assigned(p) for p in params):
            kept_ops.append(op)

    return qml.tape.QuantumTape(kept_ops, measurements)
