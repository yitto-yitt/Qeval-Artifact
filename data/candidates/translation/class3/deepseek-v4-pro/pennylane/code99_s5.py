# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    tape = circuit if hasattr(circuit, 'operations') else circuit.qtape
    new_ops = []

    for op in tape.operations:
        if op.num_params == 0:
            new_ops.append(op)
        else:
            first_param = op.data[0]
            if not qml.math.requires_grad(first_param):
                new_ops.append(op)

    return type(tape)(new_ops, tape.measurements, shots=tape.shots)
