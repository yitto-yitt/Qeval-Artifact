# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        unassigned = False
        for p in op.parameters:
            if p is None or getattr(p, "requires_grad", False):
                unassigned = True
                break
        if not unassigned:
            new_ops.append(op)

    return qml.tape.QuantumTape(new_ops, list(circuit.measurements))
