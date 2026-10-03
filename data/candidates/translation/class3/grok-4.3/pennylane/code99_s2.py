# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    ops = circuit.operations.copy()
    measurements = circuit.measurements
    new_ops = []
    for op in ops:
        params = op.parameters
        if len(params) == 0 or not isinstance(params[0], qml.operation.AnyWires):
            new_ops.append(op)
    return qml.tape.QuantumScript(new_ops, measurements)
