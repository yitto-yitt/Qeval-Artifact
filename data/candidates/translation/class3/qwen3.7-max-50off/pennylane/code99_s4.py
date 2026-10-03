# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def remove_unassigned_parameterized_gates(circuit):
    def check_unassigned(p):
        if isinstance(p, (list, tuple)):
            return any(check_unassigned(x) for x in p)
        if isinstance(p, (int, float, complex, np.number, np.ndarray, bool)):
            return False
        if hasattr(p, 'shape') or hasattr(p, 'numpy') or hasattr(p, 'item'):
            return False
        return True

    new_ops = []
    for op in circuit.operations:
        if not any(check_unassigned(p) for p in op.parameters):
            new_ops.append(op)
            
    return qml.tape.QuantumTape(new_ops, circuit.measurements)
