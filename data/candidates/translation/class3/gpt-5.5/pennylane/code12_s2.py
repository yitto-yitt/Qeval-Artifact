# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml


def get_unitary():
    def circ():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])

    return qml.matrix(circ, wire_order=[1, 0])()
