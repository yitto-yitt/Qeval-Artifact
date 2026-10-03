# EVAL_META: task_id=66, framework=pennylane, class=2
from numpy import arccos, sqrt
import pennylane as qml


def w_state():
    device = qml.device("default.qubit", wires=3)

    @qml.set_shots(shots=1)
    @qml.qnode(device)
    def circuit():
        qml.RY(2 * arccos(1 / sqrt(3)), wires=0)
        qml.ctrl(qml.Hadamard, control=0)(wires=1)
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.PauliX(wires=0)
        return qml.sample(wires=[0, 1, 2])

    return circuit
