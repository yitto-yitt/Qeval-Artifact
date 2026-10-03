# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def initialize_cnot_dihedral():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        return qml.state()

    return circuit
