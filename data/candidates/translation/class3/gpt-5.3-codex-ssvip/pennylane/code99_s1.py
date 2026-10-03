# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml


def remove_unassigned_parameterized_gates(circuit):
    ops = getattr(circuit, "operations", [])
    measurements = getattr(circuit, "measurements", [])

    def _is_unassigned_param(p):
        if hasattr(p, "name") and hasattr(p, "shape") and not isinstance(
            p, (int, float, complex, bool)
        ):
            return True
        if isinstance(p, str):
            return True
        return False

    filtered_ops = []
    for op in ops:
        params = getattr(op, "data", ())
        has_unassigned = any(_is_unassigned_param(p) for p in params)
        if not has_unassigned:
            filtered_ops.append(op)

    new_tape = qml.tape.QuantumScript(ops=filtered_ops, measurements=measurements)
    return new_tape
