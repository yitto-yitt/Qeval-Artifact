# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import sympy
import collections

def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned(param):
        if isinstance(param, sympy.Basic):
            return True
        if isinstance(param, str):
            return True
        if isinstance(param, collections.abc.Iterable) and not isinstance(param, (str, bytes)):
            try:
                for item in param:
                    if _is_unassigned(item):
                        return True
            except TypeError:
                pass
        return False

    new_ops = []
    for op in circuit.operations:
        has_unassigned = False
        for param in op.data:
            if _is_unassigned(param):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)
            
    return type(circuit)(new_ops, circuit.measurements)
