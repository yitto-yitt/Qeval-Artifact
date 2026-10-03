# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np
import numbers
import sympy

def remove_unassigned_parameterized_gates(tape):
    new_ops = []
    for op in tape.operations:
        unassigned = False
        for p in op.data:
            if isinstance(p, (sympy.Basic, str)):
                unassigned = True
                break
            if not isinstance(p, (numbers.Number, np.number, np.ndarray, list, tuple, bool)):
                if not (hasattr(p, 'shape') or hasattr(p, 'item') or hasattr(p, 'numpy')):
                    unassigned = True
                    break
        if not unassigned:
            new_ops.append(op)
            
    return qml.tape.QuantumScript(new_ops, tape.measurements)
