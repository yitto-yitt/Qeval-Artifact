# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape


def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        has_unassigned = False
        for p in op.parameters:
            if isinstance(p, qml.numpy.tensor):
                try:
                    float(p)
                except (TypeError, ValueError):
                    has_unassigned = True
                    break
            elif not isinstance(p, (int, float, complex)):
                has_unassigned = True
                break
        if not has_unassigned:
            new_ops.append(op)

    return QuantumTape(new_ops, circuit.measurements)
