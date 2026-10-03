# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import sympy
import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned(val):
        if isinstance(val, (sympy.Symbol, sympy.Basic)):
            return True
        if isinstance(val, str):
            return True
        if isinstance(val, (list, tuple, np.ndarray)):
            if isinstance(val, np.ndarray) and val.dtype != object:
                return False
            for item in val:
                if _is_unassigned(item):
                    return True
        return False

    is_list = isinstance(circuit, (list, tuple))
    ops = circuit if is_list else circuit.operations
    
    new_ops = []
    for op in ops:
        has_unassigned = False
        for param in op.parameters:
            if _is_unassigned(param):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)
            
    if is_list:
        return type(circuit)(new_ops)
    
    return circuit.__class__(ops=new_ops, measurements=circuit.measurements, prep=circuit.prep)
