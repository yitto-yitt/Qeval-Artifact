# EVAL_META: task_id=58, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def create_ch_gate():
    def ch_gate(wires):
        qml.RY(pi/4, wires=wires[1])
        qml.CNOT(wires=[wires[0], wires[1]])
        qml.RY(-pi/4, wires=wires[1])
    return ch_gate
