# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def compose_cnot_dihedral():
    dev = qml.device("default.qubit", wires=2)

    def circ1_ops():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)

    def circ2_ops():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.PauliX(wires=1)

    @qml.qnode(dev)
    def composed():
        # compose: apply elem1 first, then elem2
        circ1_ops()
        circ2_ops()
        return qml.state()

    composed_matrix = qml.matrix(
        qml.tape.QuantumTape(
            ops=[
                qml.CNOT(wires=[0, 1]),
                qml.T(wires=0),
                qml.CNOT(wires=[0, 1]),
                qml.T(wires=0),
                qml.PauliX(wires=1),
            ]
        ),
        wire_order=[0, 1],
    )

    return composed_matrix
