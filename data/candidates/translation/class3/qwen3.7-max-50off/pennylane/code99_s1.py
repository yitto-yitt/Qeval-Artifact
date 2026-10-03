# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        keep = True
        for p in op.parameters:
            if isinstance(p, (int, float, complex, np.ndarray, np.number)):
                continue
            if hasattr(p, 'item') or hasattr(p, 'numpy'):
                continue
            keep = False
            break
        if keep:
            new_ops.append(op)
    return qml.tape.QuantumTape(new_ops, circuit.measurements)
