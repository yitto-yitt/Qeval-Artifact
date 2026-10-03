# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import sympy

def remove_unassigned_parameterized_gates(circuit):
    def is_symbolic(p):
        if isinstance(p, sympy.Basic):
            return True
        if isinstance(p, (list, tuple)):
            return any(is_symbolic(x) for x in p)
        try:
            import numpy as np
            if isinstance(p, np.ndarray):
                return any(is_symbolic(x) for x in p.flat)
        except ImportError:
            pass
        return False

    new_ops = []
    for op in circuit.operations:
        if not any(is_symbolic(p) for p in op.parameters):
            new_ops.append(op)

    return type(circuit)(new_ops, circuit.measurements, prep=circuit.prep)
