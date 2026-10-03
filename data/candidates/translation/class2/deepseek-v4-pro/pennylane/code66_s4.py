# EVAL_META: task_id=66, framework=pennylane, class=2
import numpy as np
import pennylane as qml


def w_state():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.RY(2 * np.arccos(1 / np.sqrt(3)), wires=0)
        qml.CH(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.PauliX(wires=0)
        return qml.probs(wires=[0, 1, 2])

    return circuit
