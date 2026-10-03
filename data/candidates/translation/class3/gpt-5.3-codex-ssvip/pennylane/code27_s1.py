# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    ops.append(qml.Hadamard(wires=0))
    return ops
