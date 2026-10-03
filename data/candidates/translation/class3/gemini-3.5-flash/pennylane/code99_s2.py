# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import sympy
import numpy as np

def _is_symbolic(p):
    if isinstance(p, sympy.Basic):
        return True
    if isinstance(p, (list, tuple)):
        return any(_is_symbolic(x) for x in p)
    if isinstance(p, np.ndarray):
        if p.dtype == object:
            return any(_is_symbolic(x) for x in p.flat)
    return False

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        has_unassigned = False
        for p in op.data:
            if _is_symbolic(p):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)
            
    return circuit.__class__(new_ops, circuit.prep, circuit.measurements)
