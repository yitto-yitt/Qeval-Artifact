# EVAL_META: task_id=99, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from pennylane.tape import QuantumScript


def _is_assigned(param):
    try:
        float(param)
        return True
    except (TypeError, ValueError):
        pass
    try:
        arr = np.asarray(param, dtype=float)
        return arr.size >= 0
    except (TypeError, ValueError):
        return False


def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        params = op.parameters
        if len(params) == 0:
            new_ops.append(op)
            continue
        if all(_is_assigned(p) for p in params):
            new_ops.append(op)

    return QuantumScript(
        new_ops,
        measurements=list(circuit.measurements),
    )
