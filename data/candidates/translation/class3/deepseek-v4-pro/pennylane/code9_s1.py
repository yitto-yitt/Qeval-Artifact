# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_efficientSU2():
    dev = qml.device('default.qubit', wires=3)

    @qml.qnode(dev)
    def circuit(params):
        for i in range(3):
            qml.RY(params[i, 0], wires=i)
            qml.RZ(params[i, 1], wires=i)
        qml.Barrier(wires=range(3))
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 0])
        qml.Barrier(wires=range(3))
        return qml.state()

    return circuit
