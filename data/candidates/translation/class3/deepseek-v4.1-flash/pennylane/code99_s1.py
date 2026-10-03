# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        if op.parameters:
            param = op.parameters[0]
            if isinstance(param, qml.numpy.tensor) and param.requires_grad:
                continue
        new_ops.append(op)
    return QuantumScript(new_ops, circuit.measurements)
