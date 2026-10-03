# EVAL_META: task_id=9, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def create_efficientSU2():
    theta = [np.array(0.0, requires_grad=True) for _ in range(12)]

    ops = [
        qml.RY(theta[0], wires=0),
        qml.RY(theta[1], wires=1),
        qml.RY(theta[2], wires=2),
        qml.RZ(theta[3], wires=0),
        qml.RZ(theta[4], wires=1),
        qml.RZ(theta[5], wires=2),
        qml.Barrier(wires=[0, 1, 2]),
        qml.CNOT(wires=[2, 1]),
        qml.CNOT(wires=[1, 0]),
        qml.Barrier(wires=[0, 1, 2]),
        qml.RY(theta[6], wires=0),
        qml.RY(theta[7], wires=1),
        qml.RY(theta[8], wires=2),
        qml.RZ(theta[9], wires=0),
        qml.RZ(theta[10], wires=1),
        qml.RZ(theta[11], wires=2),
    ]

    circuit = qml.tape.QuantumScript(ops=ops, measurements=[])
    circuit.trainable_params = list(range(12))
    return circuit
