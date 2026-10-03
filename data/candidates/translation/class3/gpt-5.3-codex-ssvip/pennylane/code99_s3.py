# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    if not isinstance(circuit, qml.tape.QuantumTape):
        raise TypeError("Input circuit must be a PennyLane QuantumTape.")

    new_ops = []
    for op in circuit.operations:
        has_unassigned = any(
            isinstance(p, qml.numpy.tensor) and getattr(p, "requires_grad", False) and p.shape == ()
            for p in op.parameters
        )
        if not has_unassigned:
            new_ops.append(op)

    return qml.tape.QuantumTape(ops=new_ops, measurements=list(circuit.measurements))
