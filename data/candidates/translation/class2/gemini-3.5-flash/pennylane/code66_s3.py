# EVAL_META: task_id=66, framework=pennylane, class=2
import pennylane as qml
from numpy import arccos, sqrt

dev = qml.device("default.qubit", wires=3, shots=1000)


@qml.qnode(dev)
def w_state():
    qml.RY(2 * arccos(1 / sqrt(3)), wires=0)
    qml.CH(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[0, 1])
    qml.PauliX(wires=0)
    return qml.sample()
