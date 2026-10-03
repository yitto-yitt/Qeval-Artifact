# EVAL_META: task_id=66, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def w_state():
    with qml.tape.QuantumTape() as tape:
        qml.RY(2 * np.arccos(1 / np.sqrt(3)), wires=0)
        qml.CH(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.PauliX(wires=0)
        qml.sample(wires=[0, 1, 2])
    return tape
