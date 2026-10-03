# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        if not op.parameters:
            new_ops.append(op)
        elif not isinstance(op.parameters[0], qml.numpy.tensor):
            new_ops.append(op)
    return QuantumScript(new_ops, circuit.measurements)
