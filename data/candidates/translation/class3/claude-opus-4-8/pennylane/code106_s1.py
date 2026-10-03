# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def compose_cnot_dihedral():
    def circ1(state):
        qml.QubitStateVector(state, wires=[0, 1])
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        return qml.state()

    def circ2(state):
        qml.QubitStateVector(state, wires=[0, 1])
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.X(wires=1)
        return qml.state()

    dev = qml.device("default.qubit", wires=2)
    q1 = qml.QNode(circ1, dev)
    q2 = qml.QNode(circ2, dev)

    dim = 4
    u1 = np.zeros((dim, dim), dtype=complex)
    u2 = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        e = np.zeros(dim, dtype=complex)
        e[i] = 1.0
        u1[:, i] = q1(e)
        u2[:, i] = q2(e)

    composed = u2 @ u1
    return composed
