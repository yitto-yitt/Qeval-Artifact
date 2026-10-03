# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape
import numpy as np


def _is_assigned(param):
    try:
        np.asarray(param, dtype=float)
        return True
    except (TypeError, ValueError):
        return False


def remove_unassigned_parameterized_gates(circuit):
    kept_ops = []
    for op in circuit.operations:
        params = op.parameters
        if all(_is_assigned(p) for p in params):
            kept_ops.append(op)
    return QuantumTape(kept_ops, circuit.measurements, shots=circuit.shots)
