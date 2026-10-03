# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.measurements import MeasurementProcess


def remove_unassigned_parameterized_gates(circuit):
    ops = []
    measurements = []

    for op in circuit.operations:
        params = getattr(op, "data", [])
        has_unassigned = any(isinstance(p, qml.numpy.tensor) and getattr(p, "requires_grad", False) for p in params)
        has_unassigned = has_unassigned or any(isinstance(p, qml.operation.Operator) for p in params)

        if not has_unassigned:
            ops.append(op)

    measurements.extend(circuit.measurements)

    return qml.tape.QuantumScript(ops=ops, measurements=measurements, shots=circuit.shots)
