# EVAL_META: task_id=58, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def create_ch_gate():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.RY(pi / 4, wires=1)
        qml.CNOT(wires=[0, 1])
        qml.RY(-pi / 4, wires=1)
        return qml.state()

    return circuit
