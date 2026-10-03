# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, qml.QNode):
        tape = circuit.qtape
    else:
        tape = circuit

    new_ops = []
    for op in tape.operations:
        has_unassigned = False
        for param in op.parameters:
            if param is not None and qml.math.requires_grad(param):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)

    return qml.tape.QuantumTape(new_ops, tape.measurements)
