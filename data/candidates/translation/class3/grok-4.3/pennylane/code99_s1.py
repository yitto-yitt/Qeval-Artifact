# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    ops_to_keep = []
    for op in circuit.operations:
        if not any(isinstance(p, qml.operation.Parameter) for p in op.parameters):
            ops_to_keep.append(op)
    measurements = getattr(circuit, "measurements", [])
    return qml.tape.QuantumScript(ops_to_keep, measurements)
