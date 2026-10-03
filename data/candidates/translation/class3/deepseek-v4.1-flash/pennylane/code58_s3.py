# EVAL_META: task_id=58, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def create_ch_gate():
    return [
        qml.RY(pi/4, wires=1),
        qml.CNOT(wires=[0, 1]),
        qml.RY(-pi/4, wires=1)
    ]
