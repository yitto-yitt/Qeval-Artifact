# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    wires = qml.wires.Wires(range(3))
    operations = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
    ]
    dag = qml.CircuitGraph(operations, [], wires=wires)
    operations = list(dag.operations)
    operations.append(qml.Hadamard(wires=0))
    return qml.CircuitGraph(operations, [], wires=wires)
