# EVAL_META: task_id=44, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def tensor_circuits():
    dev = qml.device("default.qubit", wires=3)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=0)
        qml.CRY(0.2, wires=[1, 2])
        return qml.state()

    return circuit
