# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.operations:
        params = op.parameters
        if not (isinstance(params, qml.numpy.tensor) or 
                (len(params) > 0 and isinstance(params[0], qml.numpy.tensor) and params[0].requires_grad)):
            new_ops.append(op)
    return QuantumTape(new_ops, measurements=circuit.measurements)
