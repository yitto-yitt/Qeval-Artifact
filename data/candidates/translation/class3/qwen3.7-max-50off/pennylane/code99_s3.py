# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np
import numbers

def remove_unassigned_parameterized_gates(tape):
    new_ops = []
    for op in tape.operations:
        has_unassigned = False
        for p in op.data:
            if not isinstance(p, (numbers.Number, np.ndarray, np.number)):
                if not (hasattr(p, '__array__') or hasattr(p, 'numpy')):
                    has_unassigned = True
                    break
        if not has_unassigned:
            new_ops.append(op)
            
    return qml.tape.QuantumTape(new_ops, tape.measurements)
