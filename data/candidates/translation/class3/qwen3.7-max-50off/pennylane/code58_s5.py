# EVAL_META: task_id=58, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_ch_gate():
    with qml.tape.QuantumTape() as tape:
        qml.RY(np.pi / 4, wires=1)
        qml.CNOT(wires=[0, 1])
        qml.RY(-np.pi / 4, wires=1)
    return tape
