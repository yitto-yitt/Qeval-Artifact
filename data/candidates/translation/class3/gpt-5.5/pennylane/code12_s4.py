# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml


def get_unitary():
    wire_order = [1, 0]
    h = qml.matrix(qml.Hadamard(wires=0), wire_order=wire_order)
    cx = qml.matrix(qml.CNOT(wires=[0, 1]), wire_order=wire_order)
    return cx @ h
