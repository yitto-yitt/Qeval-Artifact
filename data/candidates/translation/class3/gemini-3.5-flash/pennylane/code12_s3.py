# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml


def get_unitary():
    def circuit():
        qml.Hadamard(wires=1)
        qml.CNOT(wires=[1, 0])

    return qml.matrix(circuit, wire_order=[0, 1])()
