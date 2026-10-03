# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def create_efficientSU2():
    weights = np.zeros((2, 3, 2), requires_grad=True)
    with qml.tape.QuantumTape() as tape:
        for i in range(3):
            qml.RY(weights[0, i, 0], wires=i)
            qml.RZ(weights[0, i, 1], wires=i)
        qml.Barrier(wires=[0, 1, 2])
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.CNOT(wires=[1, 2])
        qml.Barrier(wires=[0, 1, 2])
        for i in range(3):
            qml.RY(weights[1, i, 0], wires=i)
            qml.RZ(weights[1, i, 1], wires=i)
    return tape
