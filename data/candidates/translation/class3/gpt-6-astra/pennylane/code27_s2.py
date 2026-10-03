# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    operations = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    operations.append(qml.Hadamard(wires=0))
    return qml.CircuitGraph(
        operations,
        [],
        wires=qml.wires.Wires([0, 1, 2]),
    )
