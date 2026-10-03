# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.measurements import MeasurementProcess


def remove_unassigned_parameterized_gates(circuit):
    ops = []
    measurements = []

    for op in circuit.operations:
        has_unassigned = False
        for p in op.parameters:
            if isinstance(p, qml.numpy.tensor):
                if p.dtype == object:
                    has_unassigned = True
                    break
            elif not isinstance(p, (int, float, complex, bool)):
                has_unassigned = True
                break
        if not has_unassigned:
            ops.append(op)

    for m in circuit.measurements:
        if isinstance(m, MeasurementProcess):
            measurements.append(m)

    return qml.tape.QuantumScript(ops=ops, measurements=measurements)
