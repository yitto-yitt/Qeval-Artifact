# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []

    for op in circuit.operations:
        has_unassigned = False

        for p in op.parameters:
            if p is None or isinstance(p, str):
                has_unassigned = True
                break

            try:
                if qml.math.is_abstract(p):
                    has_unassigned = True
                    break
            except Exception:
                pass

        if not has_unassigned:
            new_ops.append(op)

    return qml.tape.QuantumTape(new_ops, circuit.measurements)
