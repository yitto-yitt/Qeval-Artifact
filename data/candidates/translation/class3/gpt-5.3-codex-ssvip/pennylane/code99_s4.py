# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
import copy

def remove_unassigned_parameterized_gates(circuit):
    new_tape = copy.copy(circuit)
    new_ops = []
    for op in circuit.operations:
        has_unassigned = False
        for p in op.parameters:
            if isinstance(p, qml.numpy.tensor):
                continue
            if not isinstance(p, (int, float, complex, bool)):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)
    new_tape._ops = new_ops
    return new_tape
