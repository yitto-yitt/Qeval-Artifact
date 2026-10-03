# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def compose_cnot_dihedral():
    def circ1():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)

    def circ2():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.PauliX(wires=1)

    U1 = qml.matrix(circ1, wire_order=[0, 1])()
    U2 = qml.matrix(circ2, wire_order=[0, 1])()

    composed_elem = U2 @ U1
    return composed_elem
